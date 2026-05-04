USER_TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImExNWQ5OGE2LTdkYzgtNDM3NS05NDk0LTEyOWJlM2RlODVkNCIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InJhZmlmYWhyZXphOSIsImVtYSI6InJhZmltZmFocmV6YUBnbWFpbC5jb20iLCJmdWwiOiJtZXBoYW50b202NjYiLCJzZXMiOiJIYkpGRFhMeUZHSk9nTEVyIiwiZHZjIjoiZjZlNWJkYTQ4NjM1YTk2NzY4ZjM4MzUyNGEwMDNmZjQiLCJ1aWQiOjIwMzUwMTksImNvdSI6IklEIn0sImV4cCI6MTc3Nzk4NjM0MiwiaWF0IjoxNzc3ODk5OTQyLCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6ImNjN2IxMDA1LWYwZTgtNGIxYi1hYjAxLWM3NDQ5MjU5MTc3ZSIsIm5iZiI6MTc3Nzg5OTk0MiwidmVyIjoidjEifQ.e7vwqhsImK70tJIIFDiI5xyTG53hc01-9vCxF41_5rPx7J9FSsqeW_poSl__ef3c8CB5kWUNjLRa8uyLnQMJSihGs3nfYNb4poZEmMyamulN34WmuiXPlkQI2F9_VW_tKHCYnIhVhLm_eo32c9Jp_p-h0pFFdn2CqUyuVtMQh_HiY3HEavUOdd9pqkhuAZ2bhu7rqsncyiYQZ8LSdARBFH4_xxYAORiEunWgEprmdM6xYGbMsmM-yU01tdO3m2YkRaBDm6DktA9_x6Vq-60AK30iCmsf5LWFqRAQfKFJ1omfc5ZUWZtA5ikzPlOiXQj95ZNrH-s5gZSoNj4rPn54ZA'
OLLAMA_KEY = '438db5eb33f94a78be649b019dfbf501.Sw4WmsByFq2yjE8_PEO4T8lb'
KEYSTATS_RESPONSE = {
    "stock_code": "<stock code being analyze>",
    "is_good_enough": "<sumary from keystats analysis, is it good or bad stock please provide yes/no/moderate only>",
    "reason": "<summary a reason why is it good or bad stock>",
    "current_valuation": {
        "summary": "<summary of the current valuation of the stock is it overvalued or undervalued or fairly valued>",
        "reason": "<reasoning for the current valuation of the stock in 1 paragraph>"
    },
    "per_share": {
        "summary": "<summary of the per share analysis is it good or bad>",
        "reason": "<reasoning for the per share analysis in 1 paragraph>"
    },
    "solvency": {
        "summary": "<summary of the solvency analysis is it good or bad>",
        "reason": "<reasoning for the solvency analysis in 1 paragraph>"
    },
    "management_effectiveness": {
        "summary": "<summary of the management effectiveness analysis is it good or bad>",
        "reason": "<reasoning for the management effectiveness analysis in 1 paragraph>"
    },
    "profitability": {
        "summary": "<summary of the profitability analysis is it good or bad>",
        "reason": "<reasoning for the profitability analysis in 1 paragraph>"
    },
    "growth": {
        "summary": "<summary of the growth analysis is it good or bad>",
        "reason": "<reasoning for the growth analysis in 1 paragraph>"
    },
    "dividend": {
        "summary": "<summary of the dividend analysis is it good or bad>",
        "reason": "<reasoning for the dividend analysis in 1 paragraph>" 
    },
    "income_statement": {
        "summary": "<summary of the income statement analysis is it good or bad>",
        "reason": "<reasoning for the income statement analysis in 1 paragraph>"
    },
    "balance_sheet": {
        "summary": "<summary of the balance sheet analysis is it good or bad>",
        "reason": "<reasoning for the balance sheet analysis in 1 paragraph>"
    },
    "cash_flow": {
        "summary": "<summary of the cash flow analysis is it good or bad>",
        "reason": "<reasoning for the cash flow analysis in 1 paragraph>"
    },
    "performance": {
        "summary": "<summary of the performance analysis is it good or bad>",
        "reason": "<reasoning for the performance analysis in 1 paragraph>"
    },
    "price_action": {
      "resistance_1": "<if any>",
      "resistance_2": "<if any>",
      "support_1": "<if any on float format>",
      "support_2": "<if any on float format>",
      "current_price": "<current price of the stock on float format>",
      "fair_value": "<the fair value of the stock on float format based on financial data above dont too far from current price>",
    },
    "summary": {
        "confidence": "<confidence level of the overall analysis on a scale of 1 to 10>",
        "overall": "<summary of the overall analysis is it good or bad stock>",
    }
}