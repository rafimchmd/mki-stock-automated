import requests
from constant.app_constant import USER_TOKEN
from datetime import datetime, timedelta
from ollama_model import get_analysis
from constant.app_constant import KEYSTATS_RESPONSE
import yfinance as yf
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

STOCK_CODE = "CUAN"

def get_buy_sell_broker(broker: str, current_date):
    last_two_weeks = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    url = f"https://exodus.stockbit.com/order-trade/broker/activity?broker_code={broker}&limit=25&page=1&from={last_two_weeks}&to={current_date}&transaction_type=TRANSACTION_TYPE_NET&market_board=MARKET_TYPE_REGULER&investor_type=INVESTOR_TYPE_ALL"

    payload = {}
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
    'authorization': f'Bearer {USER_TOKEN}',
    'origin': 'https://stockbit.com',
    'priority': 'u=1, i',
    'referer': 'https://stockbit.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    buy_stocks = []
    for item in response['data']['broker_activity_transaction']['brokers_buy']:
        stock_detail = {'stock_code': item['stock_code'], 'broker_code': item['broker_code'], 'lot': item['lot'], "avg_price": item['avg_price']}
        buy_stocks.append(stock_detail)
    return buy_stocks

def get_keystats(broker: str):
    url = f"https://exodus.stockbit.com/keystats/ratio/v1/{broker}?year_limit=10"

    payload = {}
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8,ms;q=0.7',
    'authorization': f'Bearer {USER_TOKEN}',
    'origin': 'https://stockbit.com',
    'priority': 'u=1, i',
    'referer': 'https://stockbit.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)

    return response.json()

def get_keystats_data(keystats_response: dict, stats_name: str = "Current PE Ratio (Annualised)"):
    try:
        fin_items = keystats_response['data']['closure_fin_items_results']
        for group in fin_items:
            for item in group.get('fin_name_results', []):
                fitem = item.get('fitem', {})
                if fitem.get('name') == stats_name:
                    return fitem.get('value')
    except (KeyError, TypeError):
        pass
    return None

def get_history_data(code: str):
    data = yf.Ticker(f'{code}.JK'.replace('$',''))
    hist = data.history(
        period='1mo',
        interval='1d',     
    )
    return hist.to_json()

keystats = get_keystats(f"{STOCK_CODE}")

def get_current_valuation():
    return {
        "current_valuation":
            {
                "current_pe_ratio_annualised": get_keystats_data(keystats, stats_name="Current PE Ratio (Annualised)"),
                "current_pe_ratio_ttm": get_keystats_data(keystats, stats_name="Current PE Ratio (TTM)"),
                "forward_pe_ratio": get_keystats_data(keystats, stats_name="Forward PE Ratio"),
                "ihsg_pe_ratio_ttm_median": get_keystats_data(keystats, stats_name="IHSG PE Ratio TTM (Median)"),
                "earnings_yield_ttm": get_keystats_data(keystats, stats_name="Earnings Yield (TTM)"),
                "current_price_to_sales_ttm": get_keystats_data(keystats, stats_name="Current Price to Sales (TTM)"),
                "current_price_to_book_value": get_keystats_data(keystats, stats_name="Current Price to Book Value"),
                "current_price_to_cashflow_ttm": get_keystats_data(keystats, stats_name="Current Price To Cashflow (TTM)"),
                "current_price_to_free_cashflow_ttm": get_keystats_data(keystats, stats_name="Current Price To Free CashFlow (TTM)"),
                "ev_to_ebit_ttm": get_keystats_data(keystats, stats_name="EV to EBIT (TTM)"),
                "ev_to_ebitda_ttm": get_keystats_data(keystats, stats_name="EV to EBITDA (TTM)"),
                "peg_ratio": get_keystats_data(keystats, stats_name="PEG Ratio"),
                "peg_ratio_3yr": get_keystats_data(keystats, stats_name="PEG Ratio (3yr)"),
                "peg_forward": get_keystats_data(keystats, stats_name="PEG (Forward)"),
            }
        }

def get_per_share():
    return {
        "current_per_share":
            {
                "current_eps_per_share_ttm": get_keystats_data(keystats, stats_name="Current EPS (TTM)"),
                "current_eps_per_share_annualised": get_keystats_data(keystats, stats_name="Current EPS (Annualised)"),
                "revenue_per_share_ttm": get_keystats_data(keystats, stats_name="Revenue Per Share (TTM)"),
                "cash_per_share_quarter": get_keystats_data(keystats, stats_name="Cash Per Share (Quarter)"),
                "current_book_value_per_share": get_keystats_data(keystats, stats_name="Current Book Value Per Share"),
                "free_cashflow_per_share_ttm": get_keystats_data(keystats, stats_name="Free Cashflow Per Share (TTM)"),
            }
    }

def get_solvency():
    return {
        "current_solvency":
            {
                "current_ratio_quarter": get_keystats_data(keystats, stats_name="Current Ratio (Quarter)"),
                "quick_ratio_quarter": get_keystats_data(keystats, stats_name="Quick Ratio (Quarter)"),
                "current_debt_to_equity": get_keystats_data(keystats, stats_name="Debt to Equity Ratio (Quarter)"),
                "lt_debt_to_equity": get_keystats_data(keystats, stats_name="LT Debt/Equity (Quarter)"),
                "total_liabilities_to_equity": get_keystats_data(keystats, stats_name="Total Liabilities/Equity (Quarter)"),
                "total_debt_to_total_assets": get_keystats_data(keystats, stats_name="Total Debt/Total Assets (Quarter)"),
                "financial_leverage_quarter": get_keystats_data(keystats, stats_name="Financial Leverage (Quarter)"),
                "interest_coverage_ttm": get_keystats_data(keystats, stats_name="Interest Coverage (TTM)"),
                "free_cash_flow_quarter": get_keystats_data(keystats, stats_name="Free cash flow (Quarter)"),
            }
    }

def management_effectiveness():
    return {
        "current_management_effectiveness":
            {
                "return_on_assets_ttm": get_keystats_data(keystats, stats_name="Return on Assets (TTM)"),
                "return_on_equity_ttm": get_keystats_data(keystats, stats_name="Return on Equity (TTM)"),
                "return_on_capital_employed_ttm": get_keystats_data(keystats, stats_name="Return on Capital Employed (TTM)"),
                "return_on_invested_capital_ttm": get_keystats_data(keystats, stats_name="Return On Invested Capital (TTM)"),
                "days_sales_outstanding_quarter": get_keystats_data(keystats, stats_name="Days Sales Outstanding (Quarter)"),
                "days_inventory_quarter": get_keystats_data(keystats, stats_name="Days Inventory (Quarter)"),
                "days_payables_outstanding_quarter": get_keystats_data(keystats, stats_name="Days Payables Outstanding (Quarter)"),
                "cash_conversion_cycle_quarter": get_keystats_data(keystats, stats_name="Cash Conversion Cycle (Quarter)"),
                "receivables_turnover_quarter": get_keystats_data(keystats, stats_name="Receivables Turnover (Quarter)"),
                "asset_turnover_ttm": get_keystats_data(keystats, stats_name="Asset Turnover (TTM)"),
                "inventory_turnover_ttm": get_keystats_data(keystats, stats_name="Inventory Turnover (TTM)"),
            }
    }

def get_profitability():
    return {
        "current_profitability":
            {
                "gross_profit_margin_quarter": get_keystats_data(keystats, stats_name="Gross Profit Margin (Quarter)"),
                "operating_profit_margin_quarter": get_keystats_data(keystats, stats_name="Operating Profit Margin (Quarter)"),
                "net_profit_margin_quarter": get_keystats_data(keystats, stats_name="Net Profit Margin (Quarter)"),
            }
    }

def get_stock_growth():
    return {
        "current_stock_growth":
            {
                "revenue_quarter_yoy_growth": get_keystats_data(keystats, stats_name="Revenue (Quarter YoY Growth)"),
                "gross_profit_quarter_yoy_growth": get_keystats_data(keystats, stats_name="Gross Profit (Quarter YoY Growth)"),
                "net_income_quarter_yoy_growth": get_keystats_data(keystats, stats_name="Net Income (Quarter YoY Growth)"),
            }
    }

def get_dividend():
    return {
        "current_dividend":
            {
                "dividend": get_keystats_data(keystats, stats_name="Dividend"),
                "dividend_ttm": get_keystats_data(keystats, stats_name="Dividend (TTM)"),
                "payout_ratio": get_keystats_data(keystats, stats_name="Payout Ratio"),
                "dividend_yield": get_keystats_data(keystats, stats_name="Dividend Yield"),
                "latest_dividend_ex_date": get_keystats_data(keystats, stats_name="Latest Dividend Ex-Date"),
            }
    }

def get_income_statement():
    return {
        "current_income_statement":
            {
                "revenue_ttm": get_keystats_data(keystats, stats_name="Revenue (TTM)"),
                "gross_profit_ttm": get_keystats_data(keystats, stats_name="Gross Profit (TTM)"),
                "ebitda_ttm": get_keystats_data(keystats, stats_name="EBITDA (TTM)"),
                "net_income_ttm": get_keystats_data(keystats, stats_name="Net Income (TTM)"),
            }
    }

def get_balance_sheet():
    return {
        "current_balance_sheet":
            {
                "cash_quarter": get_keystats_data(keystats, stats_name="Cash (Quarter)"),
                "total_assets_quarter": get_keystats_data(keystats, stats_name="Total Assets (Quarter)"),
                "total_liabilities_quarter": get_keystats_data(keystats, stats_name="Total Liabilities (Quarter)"),
                "working_capital_quarter": get_keystats_data(keystats, stats_name="Working Capital (Quarter)"),
                "common_equity": get_keystats_data(keystats, stats_name="Common Equity"),
                "long_term_debt_quarter": get_keystats_data(keystats, stats_name="Long-term Debt (Quarter)"),
                "short_term_debt_quarter": get_keystats_data(keystats, stats_name="Short-term Debt (Quarter)"),
                "total_debt_quarter": get_keystats_data(keystats, stats_name="Total Debt (Quarter)"),
                "net_debt_quarter": get_keystats_data(keystats, stats_name="Net Debt (Quarter)"),
                "total_equity": get_keystats_data(keystats, stats_name="Total Equity"),
            }
    }

def get_cash_flow():
    return {
        "current_cash_flow":
            {
                "cash_from_operations_ttm": get_keystats_data(keystats, stats_name="Cash From Operations (TTM)"),
                "cash_from_investing_ttm": get_keystats_data(keystats, stats_name="Cash From Investing (TTM)"),
                "cash_from_financing_ttm": get_keystats_data(keystats, stats_name="Cash From Financing (TTM)"),
                "capital_expenditure_ttm": get_keystats_data(keystats, stats_name="Capital expenditure (TTM)"),
                "free_cash_flow_ttm": get_keystats_data(keystats, stats_name="Free cash flow (TTM)"),
            }
    }

def get_performance():
    return {
        "current_performance":
            {
                "1_week_price_returns": get_keystats_data(keystats, stats_name="1 Week Price Returns"),
                "1_month_price_returns": get_keystats_data(keystats, stats_name="1 Month Price Returns"),
                "3_month_price_returns": get_keystats_data(keystats, stats_name="3 Month Price Returns"),
                "6_month_price_returns": get_keystats_data(keystats, stats_name="6 Month Price Returns"),
                "1_year_price_returns": get_keystats_data(keystats, stats_name="1 Year Price Returns"),
                "3_year_price_returns": get_keystats_data(keystats, stats_name="3 Year Price Returns"),
                "5_year_price_returns": get_keystats_data(keystats, stats_name="5 Year Price Returns"),
                "10_year_price_returns": get_keystats_data(keystats, stats_name="10 Year Price Returns"),
                "year_to_date_price_returns": get_keystats_data(keystats, stats_name="Year to Date Price Returns"),
                "52_week_high": get_keystats_data(keystats, stats_name="52 Week High"),
                "52_week_low": get_keystats_data(keystats, stats_name="52 Week Low"),
            }
    }

def generate_pdf(analysis: dict, stock_code: str):
    filename = f"data/{stock_code}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, textColor=colors.HexColor('#1a3c5e'), spaceAfter=4)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1a3c5e'), spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=14, spaceAfter=4)
    verdict_colors = {'yes': colors.HexColor('#27ae60'), 'moderate': colors.HexColor('#f39c12'), 'no': colors.HexColor('#e74c3c')}

    story = []

    # Header
    story.append(Paragraph(f"Stock Analysis Report: {stock_code}", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y %H:%M')}", styles['Normal']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#1a3c5e'), spaceAfter=8))

    # Verdict
    verdict = analysis.get('is_good_enough', '-').upper()
    verdict_color = verdict_colors.get(analysis.get('is_good_enough', '').lower(), colors.grey)
    verdict_style = ParagraphStyle('Verdict', parent=styles['Normal'], fontSize=13, textColor=verdict_color, spaceBefore=4, spaceAfter=4)
    story.append(Paragraph(f"Overall Verdict: <b>{verdict}</b>", verdict_style))
    story.append(Paragraph(analysis.get('reason', ''), body_style))
    story.append(Spacer(1, 6))

    # Sections
    sections = [
        ('current_valuation', 'Valuation'),
        ('per_share', 'Per Share'),
        ('solvency', 'Solvency'),
        ('management_effectiveness', 'Management Effectiveness'),
        ('profitability', 'Profitability'),
        ('growth', 'Growth'),
        ('dividend', 'Dividend'),
        ('income_statement', 'Income Statement'),
        ('balance_sheet', 'Balance Sheet'),
        ('cash_flow', 'Cash Flow'),
        ('performance', 'Performance'),
    ]
    for key, label in sections:
        section = analysis.get(key)
        if not section:
            continue
        story.append(Paragraph(label, section_style))
        story.append(Paragraph(f"<b>Summary:</b> {section.get('summary', '-')}", body_style))
        story.append(Paragraph(f"<b>Reason:</b> {section.get('reason', '-')}", body_style))
        story.append(HRFlowable(width='100%', thickness=0.5, color=colors.lightgrey, spaceAfter=4))

    # Price Action
    price_action = analysis.get('price_action')
    if price_action:
        story.append(Paragraph('Price Action', section_style))
        pa_data = [
            ['Metric', 'Value'],
            ['Current Price', price_action.get('current_price', '-')],
            ['Fair Value', price_action.get('fair_value', '-')],
            ['Support 1', price_action.get('support_1', '-')],
            ['Support 2', price_action.get('support_2', '-')],
            ['Resistance 1', price_action.get('resistance_1', '-')],
            ['Resistance 2', price_action.get('resistance_2', '-')],
        ]
        table = Table(pa_data, colWidths=[60*mm, 100*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3c5e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f5f9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(table)
        story.append(Spacer(1, 6))

    # Overall Summary
    summary = analysis.get('summary', {})
    if summary:
        story.append(Paragraph('Overall Summary', section_style))
        story.append(Paragraph(summary.get('overall', '-'), body_style))

    doc.build(story)
    print(f"PDF saved: {filename}")
    return filename

history_data = get_history_data(STOCK_CODE)
analysis = get_analysis(f'''You are professional money manager that analyze stock to invest, 
                        You are always success to analyze is it stock good or bad based on its financial report.
                        You are able to analyze its fair value of the stock based on its financial report.
                        You are very rich from stock market, you have a lot of experience in stock market, you have a lot of knowledge about stock market, you have a lot of knowledge about how to analyze stock, you have a lot of knowledge about how to value stock, you have a lot of knowledge about how to read financial report, you have a lot of knowledge about how to read financial statement, you have a lot of knowledge about how to read financial ratio, you have a lot of knowledge about how to read financial data, you have a lot of knowledge about how to read financial news, you have a lot of knowledge about how to read stock price movement, you have a lot of knowledge about how to read stock price action, you have a lot of knowledge about how to read stock price pattern, you have a lot of knowledge about how to read stock price trend, you have a lot of knowledge about how to read stock price support and resistance level.
                        You have access to the financial data of the stock that you will analyze, and also you have access to the historical price data of the stock that you will analyze this is the data {history_data}, you can use all of those data to analyze the stock, and also you can use your knowledge about stock analysis to analyze the stock.
                        here is the data that you can use to analyze the stock code {STOCK_CODE} in Indonesia Stock Exchange, provide analysis based on the data and also provide summary of the analysis, here is the data: {get_current_valuation()} {get_per_share()} {get_solvency()} {management_effectiveness()} {get_profitability()} {get_stock_growth()} {get_dividend()} {get_income_statement()} {get_balance_sheet()} {get_cash_flow()} {get_performance()}
                        Please provide the analysis in this format {KEYSTATS_RESPONSE}
                        ''')
print(analysis)
if analysis:
    generate_pdf(analysis, STOCK_CODE)
