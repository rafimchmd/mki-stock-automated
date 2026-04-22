USER_TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImExNWQ5OGE2LTdkYzgtNDM3NS05NDk0LTEyOWJlM2RlODVkNCIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InJhZmlmYWhyZXphOSIsImVtYSI6InJhZmltZmFocmV6YUBnbWFpbC5jb20iLCJmdWwiOiJtZXBoYW50b202NjYiLCJzZXMiOiJVSkZSOHM4NkkwNkh6TW1yIiwiZHZjIjoiZjZlNWJkYTQ4NjM1YTk2NzY4ZjM4MzUyNGEwMDNmZjQiLCJ1aWQiOjIwMzUwMTksImNvdSI6IklEIn0sImV4cCI6MTc3NjY2NjU4OSwiaWF0IjoxNzc2NTgwMTg5LCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6ImRhODE0YTYyLWQzNmQtNGJlMi1hMWY0LTg0MTg3NGExMTAwYSIsIm5iZiI6MTc3NjU4MDE4OSwidmVyIjoidjEifQ.NFO3K-EkIT0QwYl15vbZwZG4CvkzZua3VK6MmJ17p1LAK1RyRpWdEEtJXMG3d1bPJwiYetPxXsjBPki46GYmppFnPSMafbstjYwiuvaWkWOpwDrjy4S2yRvD5-cLQg8qyro3Gwd-JZ0GBHGozAq2s_oYlls_EnXO381Flam76oeCVHwae612IPTLYX6kdpimlx6i5yfj43ST4VLpEV-nB_SEgQ56orh_hf-Zw6MBSmFCi5kZKFUQNlhB_hFf9NdjBgkHsVvseiSNc19VaPyT4XrhNYA3LnjIJeExDKYXqh3-V5JuZ-S-iSBQ3kIrafuMJ53Nq2mjExdSPpE2h4So6g'
BROKER_TO_COPY = ['AK', 'BK', 'LG', 'ZP', 'AI']
OLLAMA_KEY = '438db5eb33f94a78be649b019dfbf501.Sw4WmsByFq2yjE8_PEO4T8lb'
LIST_EXPECTED_SIMILAR_STOCKS_RESPONSE = {
    "data": {
        "detail": "<list of object contain key stock_code and total_appearances and list_of_broker_code that show the stock_code>",
        "summary": "<list summary of the similar stocks that are found on each broker at least shown in 3 brokers that we want to analyze, contain response key: stock_code, broker_code, avg_price, lot, value, and total_appearances>"
    }
}
KEYSTATS_RESPONSE = {
    "stock_code": "<stock code being analyze>",
    "is_good_enough": "<sumary from keystats analysis, is it good or bad stock please provide yes/no/moderate only>",
    "reason": "<summary a reason why is it good or bad stock>"
}
WYCKOFF_RESPONSE = {
    "key_level": {
      "resistance_1": "<if any>",
      "resistance_2": "<if any>",
      "support_1": "<if any on float format>",
      "support_2": "<if any on float format>",
      "current_price": "<current price of the stock on float format>",
      "average_volume": "<calculate average volume over the period analyzed from history with format B for billion, M for million, K for thousand>"
    },
    "key_observation": "<gathered from Volume Analysis, make it simple only 2 senteces but clear>",
    "phase_identification": "<Phase A, B, C, D or E with name on wyckoff method>",
    "verdict": {
      "price_position": {
        "reading": "<gathered from accum vs dist verdict make it simple only 2 senteces but clear>",
        "points_to": "<accumulation, distribution or neutral>"
      },
      "volume_trend": {
        "reading": "<gathered from accum vs dist verdict make it simple only 2 senteces but clear>",
        "points_to": "<accumulation, distribution or neutral>"
      }
    },
    "final_assessment": {
      "scenario": "<gathered from final assessment section on Likely Scenario make it simple only 2 senteces but clear>",
      "accum": {
        "confidence": "<gathered from confidence for accumulatio in percentage>",
        "reasoning": "<gathered from reasoning for accumulation make it simple only 2 senteces but clear>"
      },
      "dist": {
        "confidence": "<gathered from confidence for distribution in percentage>",
        "reasoning": "<gathered from reasoning for distribution make it simple only 2 senteces but clear>"
      }
    },
    "scenario": {
      "accumulation": {
        "trigger": "<gathered from trading implication column trigger for bullish scenario>",
        "target": "<gathered from trading implication column target for bullish scenario>",
        "stop_loss": "<gathered from trading implication column stop loss for bullish scenario>"
      },
      "distribution": {
        "trigger": "<gathered from trading implication column trigger for bearish scenario>",
        "target": "<gathered from trading implication column target for bearish scenario>",
        "stop_loss": "<gathered from trading implication column stop loss for bearish scenario>"
      },
      "neutral": {
        "trigger": "<gathered from trading implication column trigger for neutral scenario>",
        "target": "<gathered from trading implication column target for neutral scenario>",
        "stop_loss": "<gathered from trading implication column stop loss for neutral scenario>"  
      }
    },
    "next_move": "<gathered from what to watch next section>",
    "recommendation": {
      "note": "<action to do based on the analysis>",
      "is_good_for_entry": "<gathered from my professional recommendation section with yes or no answer>",
      "entry_point": "<give the entry point range on float format and split with - if its a range if any and is_good_for_entry equals yes>",
      "stop_loss": "<give the stop loss on float format if any and is_good_for_entry equals yes maximum risk is 2%>",
      "nearest_target": "<give the target if any on float format and is_good_for_entry equals yes>",
      "reasoning": "<please provide reasoning for the recommendation given in the note section>"
    }
  }