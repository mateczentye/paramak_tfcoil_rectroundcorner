# This Dockerfile creates an enviroment with dependancies and the Paramak
# This dockerfile can be built in a few different ways.
# Docker build commands must be run from within the base repository directory
#
# There are build args availalbe for specifying the:
# - cq_version
#   The version of CadQuery to use master or 2. 
#   Default is 2.
#   Options: [master, 2]
#
# - include_neutronics
#   If software dependencies needed for neutronics simulations should be
#   included true or false.
#   Default is false.
#   Options: [true, false]
#
# - compile_cores
#   The number of CPU cores to compile the image with.
#   Default is 1.
#   Options: [1, 2, 3, 4, 5, 6...]
#
# Example builds:
# Building using the defaults (cq_version 2.1, no neutronics and 1 core compile)
# docker build -t ukaea/paramak .
#
# Building to include cadquery master, neutronics dependencies and use 8 cores.
# Run command from within the base repository directory
# docker build -t ukaea/paramak --build-arg include_neutronics=true --build-arg compile_cores=8 --build-arg cq_version=master .

# Once build the dockerimage can be run in a few different ways.
#
# Run with the following command for a terminal notebook interface
# docker run -it ukaea/paramak .
#
# Run with the following command for a jupyter notebook interface
# docker run -p 8888:8888 ukaea/paramak /bin/bash -c "jupyter notebook --notebook-dir=/examples --ip='*' --port=8888 --no-browser --allow-root"


# Once built, the docker image can be tested with either of the following commands
# docker run --rm ukaea/paramak pytest /tests
# docker run --rm ukaea/paramak  /bin/bash -c "cd .. && bash run_tests.sh"

FROM continuumio/miniconda3:4.9.2 as dependencies

# By default this Dockerfile builds with the latest release of CadQuery 2
ARG cq_version=2.1
ARG include_neutronics=false
ARG compile_cores=1

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH=/opt/openmc/bin:/opt/NJOY2016/build:$PATH \
    LD_LIBRARY_PATH=/opt/openmc/lib:$LD_LIBRARY_PATH \
    CC=/usr/bin/mpicc CXX=/usr/bin/mpicxx \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y libgl1-mesa-glx libgl1-mesa-dev libglu1-mesa-dev \
                       freeglut3-dev libosmesa6 libosmesa6-dev \
                       libgles2-mesa-dev curl && \
                       apt-get clean

# Installing CadQuery
RUN echo installing CadQuery version $cq_version && \
    conda install -c conda-forge -c python python=3.8 && \
    conda install -c conda-forge -c cadquery cadquery="$cq_version" && \
    pip install jupyter-cadquery==2.1.0 && \
    conda clean -afy

# Installing Pymoab
RUN conda install -c conda-forge moab

# Installing Paramak from Fusion-Energy repo
RUN git clone --single-branch --branch main --depth 1 https://github.com/fusion-energy/paramak.git ; \
    cd paramak ; \
    pip install e .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV OPENMC_CROSS_SECTIONS=/cross_sections.xml
ENV PATH="/MOAB/build/bin:${PATH}"
ENV PATH="/DAGMC/bin:${PATH}"

RUN mkdir /home/paramak_tfcoil_rectroundcorner
EXPOSE 8888
WORKDIR /home/paramak_tfcoil_rectroundcorner


FROM dependencies as final

COPY run_tests.sh run_tests.sh
COPY paramak_tfcoil_rectroundcorner paramak_tfcoil_rectroundcorner/
COPY setup.py setup.py
COPY tests tests/
COPY README.md README.md
COPY pytest.ini pytest.ini

# using setup.py instead of pip due to https://github.com/pypa/pip/issues/5816
RUN python setup.py install

# this helps prevent the kernal failing
RUN echo "#!/bin/bash\n\njupyter lab --notebook-dir=/home/paramak_tfcoil_rectroundcorner --port=8888 --no-browser --ip=0.0.0.0 --allow-root" >> /home/paramak_tfcoil_rectroundcorner/docker-cmd.sh
CMD bash /home/paramak_tfcoil_rectroundcorner/docker-cmd.sh
