
pytest tests/ --cov=./ --cov-report=xml

curl -Os https://uploader.codecov.io/latest/linux/codecov

chmod +x codecov
./codecov -t ${{ secrets.CODECOV_TOKEN }}