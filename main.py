import os
import pandas as pd
from supabase import create_client, client
from dotenv import load_dotenv
import gspread

load_dotenv()

pd.set_option('display.max_columns', None)

URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: client = create_client(URL, KEY)
gc = gspread.service_account(filename = "./keys.json")
SHEET = gc.open_by_url("https://docs.google.com/spreadsheets/d/1dTfqrpS_dnNqm2KJ1adsOGZHJ6PHxHIEdB6iNSKoKas/edit?gid=0#gid=0")


def query(table: str) -> dict:
    response = supabase.table(table).select("*").execute()
    return response

def to_dataframe(res: dict) -> pd.DataFrame:
    columns = list(res.data[0].keys())
    df = pd.DataFrame(res.data, columns=columns)
    return df
    
def to_csv(df: pd.DataFrame, title: str) -> None:
    df.to_csv(f"{title}.csv")

def to_sheets(df: pd.DataFrame, sheet_name: str) -> None:
  #authenticate and retrieve sheet

    df_clean = df.copy().fillna('').astype('str')

    wks = SHEET.worksheet(sheet_name)
    wks.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())


def pipeline(table_name: str):

    data = query(table_name)
    df = to_dataframe(data)

    to_csv(df, table_name)
    to_sheets(df, table_name)


if __name__ == "__main__":
    pipeline("Profiles")
    pipeline("Enrollments")
    pipeline("Sessions")




