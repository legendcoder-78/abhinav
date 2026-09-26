import json
import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ledger-iq-local-toolkit", host="127.0.0.1", port=8000)

@mcp.tool()
def save_and_format_ledgers(final_records_json: str, review_records_json: str) -> str:
    """Saves finalized and review records to local CSVs and generates a markdown table summary."""
    try:
        # Parse JSON strings into DataFrames
        final_data = json.loads(final_records_json)
        review_data = json.loads(review_records_json)
        
        final_df = pd.DataFrame(final_data)
        review_df = pd.DataFrame(review_data)
        
        # Write files directly to your local project directory
        final_df.to_csv("final_ledger.csv", index=False)
        review_df.to_csv("review_required.csv", index=False)
        
        # Generate a clean markdown summary to return to the agent
        summary = f"""### Local CSV Generation Successful!
- **`final_ledger.csv`** saved locally ({len(final_df)} rows written).
- **`review_required.csv`** saved locally ({len(review_df)} rows written).

#### Quick Preview (Final Ledger):
{final_df.head(3).to_markdown() if not final_df.empty else "No confirmed records."}
"""
        return summary
    except Exception as e:
        return f"Error processing local files: {str(e)}"

if __name__ == "__main__":
    mcp.run()