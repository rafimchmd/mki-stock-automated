USER_TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImExNWQ5OGE2LTdkYzgtNDM3NS05NDk0LTEyOWJlM2RlODVkNCIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InJhZmlmYWhyZXphOSIsImVtYSI6InJhZmltZmFocmV6YUBnbWFpbC5jb20iLCJmdWwiOiJtZXBoYW50b202NjYiLCJzZXMiOiJoeGhHRkRpa2VNTTlVUExuIiwiZHZjIjoiY2EwYTU2MDI5MDJiYzVlYjM5YTdlMWIxMDJmOWVhNTIiLCJ1aWQiOjIwMzUwMTksImNvdSI6IklEIn0sImV4cCI6MTc3NjYwMzgxNSwiaWF0IjoxNzc2NTE3NDE1LCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6IjVjMGU4ZjE1LTRmYTMtNDY2YS05MmFmLTM2NTg0ZjQ0NmUyMyIsIm5iZiI6MTc3NjUxNzQxNSwidmVyIjoidjEifQ.eJ39hYj6eVirhM1bXS3VXtGWRbF4FzkoA5UY_-hxJyC6TmxcIu1Ub-VrpilG1l9IACQoRhsjm_8yhzpBAMxcwePcaLcvQeYAhyEG2bq_Jc3G5s-NJizDiYmiELR1ms4vGimfJ70ibD7DaqYVHVe_ULmOd2ZKdlkFDTBL2Pk_G3tnYL7fIz_RGwPxxVsUQcZJR9qTvyJumeJ5ShUO3iMcgS6TVkARspnPt-qHxP9S4PSsYNQIgbaEOtJQN4A9msrx8WE-X9wWX4fwjeGaY_jOSlR2iBaThu0PDb1KToGlCH83zQaaNax4lgelLc-enSJ1Q2C_BW10oRsB35n0NUwwkg'
BROKER_TO_COPY = ['AK', 'BK', 'LG', 'ZP', 'AI']
OLLAMA_KEY = '438db5eb33f94a78be649b019dfbf501.Sw4WmsByFq2yjE8_PEO4T8lb'
LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE = {
    "data": {
        "detail": "<list of object contain key stock_code and total_appearances and list_of_broker_code that show the stock_code>",
        "summary": "<list summary of the similar stocks that are found on each broker at least shown in 3 brokers that we want to analyze, contain response key: stock_code, broker_code, avg_price, lot, value, and total_appearances>"
    }
}