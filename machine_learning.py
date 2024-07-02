import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error



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
    
    return sum(aps) / len(aps), aps, pd.concat(all_predictions)


def machine_learning():
    stats = pd.read_csv('player_mvp_stats.csv')
    del stats['Unnamed: 0']
    stats = stats.fillna(0)
    predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',    
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year', 'W', 'L', 'W/L%', 'GB', 'PS/G',  
       'PA/G', 'SRS']
    
    # train = stats[stats['Year'] < 2024]
    # test = stats[stats['Year'] == 2024]

    reg = Ridge(alpha=.1)

    # reg.fit(train[predictors], train['Share']) 
    # predictions = reg.predict(test[predictors])
    # predictions =pd.DataFrame(predictions, columns=['predictions'], index=test.index)

    # combination = pd.concat([test[['Player','Share']],predictions], axis=1)

    #print(combination.sort_values('Share',ascending=False).head(10))

    #print(mean_squared_error(combination['Share'], combination['predictions']))
    
    # combination = combination.sort_values('Share', ascending=False)
    # combination['Rk'] = list(range(1,combination.shape[0]+1))
    # #print(combination.head(10))
    # combination = combination.sort_values('predictions', ascending=False)
    # combination['Predicted_Rk'] = list(range(1,combination.shape[0]+1))
    #print(combination.head(10))

    #print(combination.sort_values('Share',ascending=False).head(10))

    #print(find_ap(combination))

    years = list(range(1991,2025))
    # aps = []
    # all_predictions = []
    # for year in years[5:]:
    #     train = stats[stats['Year'] < year]
    #     test = stats[stats['Year'] == year]
    #     reg.fit(train[predictors],train['Share'])
    #     predictions = reg.predict(test[predictors])
    #     predictions =pd.DataFrame(predictions, columns=['predictions'], index=test.index)
    #     combination = pd.concat([test[['Player','Share']],predictions], axis=1)

    #     all_predictions.append(combination)
    #     aps.append(find_ap(combination))
        
    #print(sum(aps) / len(aps)), performance using all of the data
        
    # ranking = add_ranks(all_predictions[1])
    # print(ranking[ranking['Rk'] < 6].sort_values('Diff', ascending=False))

    mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)
    #print(mean_ap)
    #print(all_predictions[all_predictions['Rk'] <= 5].sort_values('Diff').head(10))
    #print(pd.concat([pd.Series(reg.coef_), pd.Series(predictors)], axis=1).sort_values(0, ascending=False))#Which columns does the model think is the most important
    stats_ratios = stats[['PTS','AST','STL','BLK','3P','Year']].groupby('Year').apply(lambda x: x/x.mean())
    #print(stats_ratios)
        
    
    






if __name__ == "__main__":
    main() 