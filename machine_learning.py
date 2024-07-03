import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor



def main():
    machine_learning()
    print('main')

def find_ap(combination):
    actual = combination.sort_values('Share',ascending=False).head(5)
    predicted = combination.sort_values('predictions',ascending=False)
    ps = []
    found = 0
    seen = 1
    for index,row in predicted.iterrows():
        if row['Player'] in actual['Player'].values:
            found += 1
            ps.append(found/seen)
        seen += 1
    return sum(ps) / len(ps)

def add_ranks(combination):
    combination = combination.sort_values('Share', ascending=False)
    combination['Rk'] = list(range(1,combination.shape[0]+1))
    combination = combination.sort_values('predictions', ascending=False)
    combination['Predicted_Rk'] = list(range(1,combination.shape[0]+1))

    combination['Diff'] = combination['Rk'] - combination['Predicted_Rk']
    return combination

def backtest(stats,model, year, predictors):
    years = list(range(1991,2025))
    aps = []
    all_predictions = []
    for year in years[5:]:
        train = stats[stats['Year'] < year]
        test = stats[stats['Year'] == year]
        model.fit(train[predictors],train['Share'])
        predictions = model.predict(test[predictors])
        predictions =pd.DataFrame(predictions, columns=['predictions'], index=test.index)
        combination = pd.concat([test[['Player','Share']],predictions], axis=1)
        combination = add_ranks(combination)
        all_predictions.append(combination)
        aps.append(find_ap(combination))
    print(combination.sort_values('Share',ascending=False).head(5))
    
    return sum(aps) / len(aps), aps, pd.concat(all_predictions)


def machine_learning():
    stats = pd.read_csv('player_mvp_stats.csv')
    del stats['Unnamed: 0']
    stats = stats.fillna(0)
    predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',    
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year', 'W', 'L', 'W/L%', 'GB', 'PS/G',  
       'PA/G', 'SRS']

    reg = Ridge(alpha=.1)
    rf = RandomForestRegressor(n_estimators=100, random_state=1, min_samples_split=5)

    years = list(range(1991,2025))

    #print(all_predictions[all_predictions['Rk'] <= 5].sort_values('Diff').head(10))
    #print(pd.concat([pd.Series(reg.coef_), pd.Series(predictors)], axis=1).sort_values(0, ascending=False))#Which columns does the model think is the most important
    stat_ratios = stats[['PTS','AST','STL','BLK','3P','Year']].groupby('Year', group_keys=False).apply(lambda x: x/x.mean())
    stat_ratios = stat_ratios.reset_index(drop=True)  # Reset the index

    # Ensure the index matches with stats before assignment
    stats = stats.reset_index(drop=True)  # Reset the index
    stats[['PTS_R','AST_R','STL_R','BLK_R','3P_R']] = stat_ratios[['PTS','AST','STL','BLK','3P']]
    predictors += ['PTS_R','AST_R','STL_R','BLK_R','3P_R']
    #mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)
    stats['NPos'] = stats['Pos'].astype('category').cat.codes
    stats['NPTm'] = stats['Tm'].astype('category').cat.codes

    #mean_ap, aps, all_predictions = backtest(stats, rf, years[28:], predictors)
    #print(mean_ap)

    mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)
    print(mean_ap)
        
    
    






if __name__ == "__main__":
    main() 