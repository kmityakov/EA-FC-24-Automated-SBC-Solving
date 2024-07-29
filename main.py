import input
import optimize
import pandas as pd

from read_sbc_requirements import get_challenge_requirements
from save_squad_lib import save_squad

# Preprocess the club dataset obtained from https://github.com/ckalgos/fut-trade-enhancer.
def preprocess_data_1(df: pd.DataFrame):
    df = df.drop(['Price Range', 'Bought For', 'Discard Value', 'Contract Left'], axis = 1)
    df = df.rename(columns={'Player Name': 'Name', 'Nation': 'Country', 'Quality': 'Color', 'FUTBIN Price': 'Cost'})
    df = df[df["IsUntradable"] == True]
    df = df[df["IsLoaned"] == False]
    df = df[df["Cost"] != '--NA--']
    # Note: The filter on rating is especially useful when there is only a single constraint like Squad Rating: Min XX.
    # Otherwise, the search space is too large and this overwhelms the solver (very slow in improving the bound).
    # df = df[(df["Rating"] >= input.SQUAD_RATING - 3) & (df["Rating"] <= input.SQUAD_RATING + 3)]
    df = df.reset_index(drop = True).astype({'Rating': 'int32', 'Cost': 'int32'})
    return df

# Preprocess the club dataset obtained from https://chrome.google.com/webstore/detail/fut-enhancer/boffdonfioidojlcpmfnkngipappmcoh.
# Datset obtained from here has the extra columns [IsDuplicate, IsInActive11].
# So duplicates can be prioritized now if needed.
def preprocess_data_2(df: pd.DataFrame):
    # df = df.drop(['Price Limits', 'Last Sale Price', 'Discard Value', 'Contract', 'DefinitionId'], axis = 1)
    df = df.drop(['Price Limits', 'Last Sale Price', 'Discard Value', 'Contract'], axis=1)
    df = df.rename(columns={'Nation': 'Country', 'Team' : 'Club', 'ExternalPrice': 'Cost'})
    df["Color"] = df["Rating"].apply(lambda x: 'Bronze' if x < 65 else ('Silver' if 65 <= x <= 74 else 'Gold'))
    df.insert(2, 'Color', df.pop('Color'))
    df = df[df["Rarity"] != 'Centurions Evo']
    df = df[df["Rarity"] != 'Complete Founder Evolution']
    df = df[df["Rarity"] != 'Evolutions III']
    df = df[df["Rarity"] != 'Winter Wildcards Evo']

    # df = df[(df["Untradeable"] == True) | (df["Color"] != 'Gold')]
    df = df[df["IsInActive11"] != True]
    df = df[df["Loans"] == False]
    df = df[df["Cost"] != '-- NA --']
    df = df[(df["Cost"] != '0') & (df["Cost"] != 0)]
    if input.MIN_RATING > 0:
        df = df[df["Rating"] >= input.MIN_RATING]
    if input.MAX_RATING > 0:
        df = df[df["Rating"] <= input.MAX_RATING]
    # Note: The filter on rating is especially useful when there is only a single constraint like Squad Rating: Min XX.
    # Otherwise, the search space is too large and this overwhelms the solver (very slow in improving the bound).
    # df = df[(df["Rating"] >= input.SQUAD_RATING - 3) & (df["Rating"] <= input.SQUAD_RATING + 3)]
    if input.USE_PREFERRED_POSITION:
        df = df.rename(columns={'Preferred Position': 'Position'})
        df.insert(4, 'Position', df.pop('Position'))
    elif input.USE_ALTERNATE_POSITIONS:
        df = df.drop(['Preferred Position'], axis = 1)
        df = df.rename(columns={'Alternate Positions': 'Position'})
        df.insert(4, 'Position', df.pop('Position'))
        df['Position'] = df['Position'].str.split(',')
        df = df.explode('Position') # Creating separate entries of a particular player for each alternate position.
    df = df.reset_index(drop = True).astype({'Rating': 'int32', 'Cost': 'int32'})
    return df

# dataset = "AC Margheriti.csv"
input.DATASET = "LiverKlopp.csv"
# input.DATASET = "AC Margheriti.csv"
if __name__ == "__main__":
    get_challenge_requirements(754,1949)

    df = pd.read_csv(input.DATASET, index_col = False)
    # df = preprocess_data_1(df)
    df = preprocess_data_2(df)
    # df.to_excel("Club_Pre_Processed.xlsx", index = False) # This could be used to fix certain players and optimize the rest.
    final_players = optimize.SBC(df)
    if final_players:
        df_out = df.iloc[final_players]
        df_out.insert(5, 'Is_Pos', df_out.pop('Is_Pos'))
        print(f"Total Chemistry: {df_out['Chemistry'].sum()}")
        squad_rating = input.calc_squad_rating(df_out["Rating"].tolist())
        print(f"Squad Rating: {squad_rating}")
        print(f"Total Cost: {df_out['Cost'].sum()}")
        # df_out.to_excel("output.xlsx", index = False)
        df_out.to_csv("output.csv", index=False)
        save_squad(df_out)
