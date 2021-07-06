
pytest tests/ --cov=./ --cov-report=xml

curl -Os https://uploader.codecov.io/latest/linux/codecov

chmod +x codecov
./codecov -t ${8cd3ec3f-7b8a-440b-bfec-7e61478c41e8}