import json
import ccxt
import time

from ascii_graph.colors import *
from ascii_graph import Pyasciigraph
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

from terminaltables import AsciiTable

from config import CondexConfig

from models.TickerModel import TickerModel
from models.IndexInfoModel import IndexInfoModel
from models.IndexedCoinModel import IndexedCoinModel
from models.CoinBalanceModel import CoinBalanceModel
from models.SupportedCoinModel import SupportedCoinModel

from managers.DatabaseManager import DatabaseManager

class ShowCommandManager:

    def __init__(self):
        pass

    def show_avalible_coins(self):

        table_data = [['Avalible','Coins','.','.','.','.','.','.','.','.','.']]

        count = 0
        current_array = []
        
        for coin in SupportedCoinModel.select():
            
            current_array.append(coin.Ticker)

            if count == 10:
                table_data.append(current_array)
                current_array = []
                count = 0
            else:
                count = count + 1

        table = AsciiTable(table_data)

        print table.table

    def show_stats(self):
        indexInfo = IndexInfoModel.get(id=1)

        # Create the Index Table
        cointTableData =[['Coin', 'Amount', 'BTC Val', 'USD Val', 'Desired %', 'Locked', 'Active %', 'U Gain %', 'R Gain %']]

        for coin in IndexedCoinModel.select():

            coinBalance = CoinBalanceModel.get(CoinBalanceModel.Coin==coin.Ticker)
            realizedGainModel = DatabaseManager.get_realized_gain_model(coin.Ticker)

            newArray = [coin.Ticker, coinBalance.TotalCoins, coinBalance.BTCBalance, round(coinBalance.USDBalance,2), coin.DesiredPercentage, coin.Locked, coin.CurrentPercentage, coin.UnrealizedGain, realizedGainModel.RealizedGain, ]
            cointTableData.append(newArray)

        # Create the summary table
        summary_table_data = [['Active', 'Index Count', 'BTC Val', 'USD Val', 'Unrealized Gain %', 'Realized Gain %']]
        summary_table_data.append([True, len(IndexedCoinModel.select()), indexInfo.TotalBTCVal, indexInfo.TotalUSDVal, round(indexInfo.TotalUnrealizedGain,2), round(indexInfo.TotalRealizedGain,2)])

        coin_table = AsciiTable(cointTableData)
        summary_table = AsciiTable(summary_table_data)

        print "\nCurrent Index Summary"
        print summary_table.table

        print "\nCurrent Index Table"
        print coin_table.table

    def show_index(self):
        graphArray = []

        for coin in IndexedCoinModel.select():
            graphArray.append((coin.Ticker, coin.DesiredPercentage))

        pyGraph = Pyasciigraph(
            line_length=50,
            min_graph_length=50,
            separator_length=4,
            multivalue=False,
            human_readable='si',
            graphsymbol='*',
            float_format='{0:,.2f}'
            )

        thresholds = {
          15:  Gre, 30: Blu, 50: Yel, 60: Red,
        }
        data = hcolor(graphArray, thresholds)


        print "\n"
        for line in  pyGraph.graph('Index Distribution', data=data):
            print(line)
        print "\n"
