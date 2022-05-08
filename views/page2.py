import sys
from tkinter import SCROLL
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from server import app, User
import plotly.express as px
import pandas as pd
from collections import OrderedDict
import json
from random import randint
from numpy.random import normal
from collections import defaultdict, OrderedDict, deque
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import time
import math
from bintrees import RBTree
from io import StringIO
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import dash_loading_spinners as dls
import plotly.io as pio

SCROLL = {
    "margin-top": "50%",
    "padding": "25%",
  
}
layout = html.Div([
                html.H1('Parameter'),
                dbc.Row(dbc.Col(html.Div(
                    html.H4(dbc.Badge("PROTOCOL", color="primary", className="me-1"))
                ))),
                dbc.Row(
                    [
                        dbc.Col(html.Div(html.P("Bond Expiry"))),
                        dbc.Col(html.Div(html.P("Bond Delay"))),
                        dbc.Col(html.Div(html.P("Bond Range"))),
                        dbc.Col(html.Div(html.P())),
                        dbc.Col(html.Div(html.P("Trades per Day"))),
            ]
        ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="1-100",  value = 60, id = "bond expiry"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="",  value = 15000, id = "bond delay"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0.9, id = "bond range min"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Max", value = 1.1, id = "bond range max"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Max", value = 15000, id = "trades per day"))),
            ]
        ), 
                 dbc.Row([dbc.Col(html.Div(html.P()))
            ]
        ),
                dbc.Row(dbc.Col(html.Div(
                    html.H4(dbc.Badge("MARKET", color="success", className="me-2"))
                ))),

                dbc.Row(
                    [
                        dbc.Col(html.Div(html.P("Base Spread"))),
                        dbc.Col(html.Div(html.P("Price Noise"))),
                        dbc.Col(html.Div(html.P("Vol MA Step"))),
                        dbc.Col(html.Div(html.P("Price MA Step"))),
                        dbc.Col(html.Div(html.P("Market Speed"))),
            ]
        ),
                 dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100",value = 1e-3, id = "base spread"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 1e-4, id = "price noise"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 1000, id = "vol ma step"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 1000, id = "price ma step"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0.4, id = "market speed"))),
            ]
        ),

                dbc.Row([dbc.Col(html.Div(html.P()))
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(html.P("Price Scale"))),
                        dbc.Col(html.Div(html.P("Var Scale"))),
                        dbc.Col(html.Div(html.P())),
                        dbc.Col(html.Div(html.P())),
                        dbc.Col(html.Div(html.P())),
            ]
        ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 1e-4, id = "price scale"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 0, id = "var scale"))),
                        dbc.Col(html.Div()),
                        dbc.Col(html.Div()),
                        dbc.Col(html.Div()),
            ]
        ),
          
                dbc.Row([dbc.Col(html.Div(html.P()))
            ]
        ),
                dbc.Row(dbc.Col(html.Div(
                    html.H4(dbc.Badge("TRADER", color="danger", className="me-3"))
                ))),

                dbc.Row(
                    [
                        dbc.Col(html.Div(html.P("Ideal Trader"))),
                        dbc.Col(html.Div(html.P("Average Trader"))),
                        dbc.Col(html.Div(html.P("Basic Trader"))),
                        dbc.Col(html.Div(html.P("Num Order Live"))),
                        dbc.Col(html.Div(html.P("Track Freq"))),
            ]
        ),
                 dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 5,id = "ideal trader"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 500,  id = "average trader"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Min", value = 100,  id = "basic trader"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100",value = 300000,  id = "num order live"))),
                        dbc.Col(html.Div(dbc.Input(type="number",placeholder="Masukkan angka antara 1-100", value = 15, id = "track freq"))),
                
            ]
        ),
        
          
                dbc.Row([dbc.Col(html.Div(html.H1()))
            ]
        ),
                dbc.Row([dbc.Col(html.Div(html.H1()))
            ]
        ),
                dbc.Row([dbc.Col(html.Div(
                    html.A(dbc.Button("SUBMIT", color="info", size="lg", className="me-1",id='btn-submit'), href="#simulasi")
                ))
            ]
        ),
                dcc.Store(id='data'),

                dbc.Container([
                    html.H3(dbc.Badge('Simulation Result',color="info", id="simulasi")),
                    dbc.Spinner([
                            dcc.Location(id="loading"),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='grafik7')),
                                dbc.Col(dcc.Graph(id='grafik1'))]),
                            dbc.Row([                
                                dbc.Col(dcc.Graph(id='grafik8')),
                                dbc.Col(dcc.Graph(id='grafik3'))]),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='grafik2')),
                                dbc.Col(dcc.Graph(id='grafik4'))]),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='grafik5')),
                                dbc.Col(dcc.Graph(id='grafik6'))])
                        ], spinner_style={"width": "5rem", "height": "5rem"}, color="primary")

                ])    ,
                # html.Div([

        # ],
        #     id="loading",style=SCROLL
        # ),
        
        
                ] )



@app.callback(Output('data', 'data'),Output('grafik1', 'figure'),Output('grafik7', 'figure'),Output('grafik8', 'figure'),
                [Input('btn-submit', 'n_clicks')],
                [State('bond expiry', 'value'),State('bond delay', 'value'),State('bond range min', 'value'),State('bond range max', 'value'),State('trades per day', 'value'),
                State('base spread', 'value'),State('price noise', 'value'),State('vol ma step', 'value'),State('price ma step', 'value'),State('market speed', 'value'),State('price scale', 'value'),State('var scale', 'value'),
                State('ideal trader', 'value'),State('average trader', 'value'),State('basic trader', 'value'),State('num order live', 'value'),State('track freq', 'value')])


def update_output(clicked, input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12, input13, input14, input15, input16, input17):
    if clicked is None:
        raise PreventUpdate
    if clicked:

                    # ETH trading settings
        ETH_DAY_OFFSET = 0
        TRADES_PER_DAY = input5

        # BOND settings
        BOND_EXPIRY = input1 * (30 * 24 * 60 * 60)
        BOND_DELAY = input2 # Steps 
        BOND_RANGE = (input3,input4)

        # MARKET price settings 
        BASE_SPREAD = input6 # 0.1% 
        PRICE_NOISE = input7
        VOL_MA_STEPS = input8
        PRICE_MA_STEPS = input9
        MARKET_SPEED = input10

        # DEMAND ratio settings
        PRICE_SCALE = input11
        VAR_SCALE = input12

        # TRADER settings
        BASIC_TRADER_THRESHOLD = 0.05 # trades when BAS < 0.95 or BAS > 1.05

        # TRADER demographics 
        trader_demographics = OrderedDict()
        trader_demographics['IdealTrader'] = input13
        trader_demographics['AverageTrader'] = input14
        trader_demographics['BasicTrader'] = input15
        trader_demographics['InvestorTrader'] = 10

        # SIMULATION SETTINGS 
        NUM_ORDERS_INIT = input9 * 3
        NUM_ORDERS_LIVE = input16

        # TRACKING settings 
        TRACK_FREQ = input17 # Track every 50 steps
        # for auto-reloading external modules


        ######

        def biased_coin(prob):
            return int(np.random.random() < prob)

        def clamp_bas_price(price):
            # 1 BAS = price ETH
            return np.clip(price, 0, 10.0)

        def clamp_bas_qty(qty): 
            # Max order size of $100,000
            return np.clip(qty, 0, 1e5)

        def months_to_seconds(mths):
            return mths * 30 * 24 * 60 * 60

        eth_prices = json.load(open('/mnt/c/Users/Muhamad Thoriq/onedrive/documents/muhamad thoriq/ta/bismillah/dash-flask-login-master/views/etherium1.json'))

        def get_eth_price(t):
            idx = ETH_DAY_OFFSET + (t // TRADES_PER_DAY)
            lin = (t % TRADES_PER_DAY) / (1. * TRADES_PER_DAY)
            if idx >= len(eth_prices) - 1:
                return eth_prices[-1]
            return eth_prices[idx] * (1.0 - lin) + eth_prices[idx + 1] * lin


        #####
        ##PYLOB
        class Order(object):
            def __init__(self, quote, orderList):
                self.timestamp = int(quote['timestamp'])
                self.qty = int(quote['qty'])
                self.price = quote['price']
                self.idNum = quote['idNum']
                self.tid = quote['tid']
                self.nextOrder = None
                self.prevOrder = None
                self.orderList = orderList
            
            def nextOrder(self):
                return self.nextOrder
            def prevOrder(self):
                return self.prevOrder

            def updateQty(self, newQty, newTimestamp):
                if newQty > self.qty and self.orderList.tailOrder != self:
                    ## Move order to end of the tier (loses time priority)            
                    self.orderList.moveTail(self)
                self.orderList.volume -= self.qty-newQty
                self.timestamp = newTimestamp
                self.qty = newQty

            def __str__(self):
                return "%s\t@\t%.4f\tt=%d" % (self.qty, self.price, self.timestamp)

                '''
            Created on Mar 22, 2013

            @author: Ash Booth
        '''

        class OrderList(object):
            def __init__(self):
                self.headOrder = None
                self.tailOrder = None
                self.length = 0
                self.volume = 0    # Total share volume
                self.last = None
                
            def __len__(self):
                return self.length
            
            def __iter__(self):
                self.last = self.headOrder
                return self
            
            def next(self):
                if self.last == None:
                    raise StopIteration
                else:
                    returnVal = self.last
                    self.last = self.last.nextOrder
                    return returnVal
            
            def __next__(self):
                return self.next()

            def getHeadOrder(self):
                return self.headOrder
            
            def appendOrder(self, order):
                if len(self) == 0:
                    order.nextOrder = None
                    order.prevOrder = None
                    self.headOrder = order
                    self.tailOrder = order
                else:
                    order.prevOrder = self.tailOrder
                    order.nextOrder = None
                    self.tailOrder.nextOrder = order
                    self.tailOrder = order
                self.length += 1
                self.volume += order.qty
                
            def removeOrder(self, order):
                self.volume -= order.qty
                self.length -= 1
                if len(self) == 0:
                    return
                # Remove from list of orders
                nextOrder = order.nextOrder
                prevOrder = order.prevOrder
                if nextOrder != None and prevOrder != None:
                    nextOrder.prevOrder = prevOrder
                    prevOrder.nextOrder = nextOrder
                elif nextOrder != None:
                    nextOrder.prevOrder = None
                    self.headOrder = nextOrder
                elif prevOrder != None:
                    prevOrder.nextOrder = None
                    self.tailOrder = prevOrder
                    
            def moveTail(self, order):
                if order.prevOrder != None:
                    order.prevOrder.nextOrder = order.nextOrder
                else:
                    # Update the head order
                    self.headOrder = order.nextOrder
                order.nextOrder.prevOrder = order.prevOrder
                # Set the previous tail order's next order to this order
                self.tailOrder.nextOrder = order
                order.prevOrder = self.tailOrder
                self.tailOrder = order
                order.nextOrder = None
                
            def __str__(self):
                from io import StringIO
                file_str = StringIO()
                for order in self:
                    file_str.write("%s\n" % str(order))
                return file_str.getvalue()



        class OrderTree(object):
            def __init__(self):
                self.priceTree = RBTree()
                self.priceMap = {}  # Map from price -> orderList object
                self.orderMap = {}  # Order ID to Order object
                self.volume = 0     # How much volume on this side?
                self.nOrders = 0   # How many orders?
                self.lobDepth = 0  # How many different prices on lob?
                
            def __len__(self):
                return len(self.orderMap)
            
            def getPrice(self, price):
                return self.priceMap[price]
            
            def getOrder(self, idNum):
                return self.orderMap[idNum]
            
            def createPrice(self, price):
                self.lobDepth += 1
                newList = OrderList()
                self.priceTree.insert(price, newList)
                self.priceMap[price] = newList
                
            def removePrice(self, price):
                self.lobDepth -= 1
                self.priceTree.remove(price)
                del self.priceMap[price]
                
            def priceExists(self, price):
                return price in self.priceMap
            
            def orderExists(self, idNum):
                return idNum in self.orderMap
            
            def insertOrder(self, quote):
                if self.orderExists(quote['idNum']):
                    self.removeOrderById(quote['idNum'])
                self.nOrders += 1
                if quote['price'] not in self.priceMap:
                    self.createPrice(quote['price'])
                order = Order(quote, self.priceMap[quote['price']])
                self.priceMap[order.price].appendOrder(order)
                self.orderMap[order.idNum] = order
                self.volume += order.qty
                
            def updateOrder(self, orderUpdate):
                order = self.orderMap[orderUpdate['idNum']]
                originalVolume = order.qty
                if orderUpdate['price'] != order.price:
                    # Price changed
                    orderList = self.priceMap[order.price]
                    orderList.removeOrder(order)
                    if len(orderList) == 0:
                        self.removePrice(order.price) 
                    self.insertOrder(orderUpdate)
                else:
                    # Quantity changed
                    order.updateQty(orderUpdate['qty'], orderUpdate['timestamp'])
                self.volume += order.qty-originalVolume
                
            def removeOrderById(self, idNum):
                self.nOrders -= 1
                order = self.orderMap[idNum]
                self.volume -= order.qty
                order.orderList.removeOrder(order)
                if len(order.orderList) == 0:
                    self.removePrice(order.price)
                del self.orderMap[idNum]
                
            def maxPrice(self):
                if self.lobDepth > 0:
                    return self.priceTree.max_key()
                else: return None
            
            def minPrice(self):
                if self.lobDepth > 0:
                    return self.priceTree.min_key()
                else: return None
            
            def maxPriceList(self):
                if self.lobDepth > 0:
                    return self.getPrice(self.maxPrice())
                else: return None
            
            def minPriceList(self):
                if self.lobDepth > 0:
                    return self.getPrice(self.minPrice())
                else: return None



        # BAS / ETH. Price ~ 0.10 right now 
        class OrderBook(object):
            def __init__(self, tick_size = 0.0001):
                self.tape = deque(maxlen=None) # Index [0] is most recent trade
                self.bids = OrderTree()
                self.asks = OrderTree()
                self.lastTick = None
                self.lastTimestamp = 0
                self.tickSize = tick_size
                self.time = 0
                self.nextQuoteID = 0
                self.traderPool = {}
                
            def clipPrice(self, price):
                """ Clips the price according to the ticksize """
                return round(price, int(math.log10(1 / self.tickSize)))
            
            def updateTime(self):
                self.time+=1
            
            def setTraderPool(self, traderPool):
                self.traderPool = traderPool

            def processOrder(self, quote, fromData=False, verbose=False):
                orderType = quote['type']
                orderInBook = None
                if fromData:
                    self.time = quote['timestamp']
                else:
                    self.updateTime()
                    quote['timestamp'] = self.time
                if quote['qty'] <= 0:
                    sys.exit('processLimitOrder() given order of qty <= 0')
                if not fromData: self.nextQuoteID += 1

                # user = quote['user_key']
                # if quote['side'] == 'ask':
                #     if self.balances['bas'][user] < quote['qty']:
                #         assert(False, "Trying to sell more than the person has")
                # else: # quote['side'] == 'bid'
                #     if self.balances[]

                if orderType=='market':
                    trades = self.processMarketOrder(quote, verbose)
                elif orderType=='limit':
                    quote['price'] = self.clipPrice(quote['price'])
                    trades, orderInBook = self.processLimitOrder(quote, fromData, verbose)
                else:
                    sys.exit("processOrder() given neither 'market' nor 'limit'")
                return trades, orderInBook
            



            def processOrderList(self, side, orderlist, qtyStillToTrade, quote, verbose):
                '''
                Takes an order list (stack of orders at one price) and 
                an incoming order and matches appropriate trades given 
                the orders quantity.
                '''
                trades = []
                qtyToTrade = qtyStillToTrade
                while len(orderlist) > 0 and qtyToTrade > 0:
                    headOrder = orderlist.getHeadOrder()
                    tradedPrice = headOrder.price
                    counterparty = headOrder.tid
                    # Can fill the order given fully, with an existing order partially. 
                    if qtyToTrade < headOrder.qty:
                        tradedQty = qtyToTrade
                        # Amend book order
                        newBookQty = headOrder.qty - qtyToTrade
                        headOrder.updateQty(newBookQty, headOrder.timestamp)
                        # Incoming done with
                        qtyToTrade = 0
                    elif qtyToTrade == headOrder.qty:
                        tradedQty = qtyToTrade
                        if side=='bid':
                            # Hit the bid
                            self.bids.removeOrderById(headOrder.idNum)
                        else:
                            # Lift the ask
                            self.asks.removeOrderById(headOrder.idNum)
                        # Incoming done with
                        qtyToTrade = 0
                    else:
                        tradedQty = headOrder.qty
                        if side=='bid':
                            # Hit the bid
                            self.bids.removeOrderById(headOrder.idNum)
                        else:
                            # Lift the ask
                            self.asks.removeOrderById(headOrder.idNum)
                        # We need to keep eating into volume at this price
                        qtyToTrade -= tradedQty

                    if verbose: print('>>> TRADE \nt=%d $%f n=%d p1=%d p2=%d' % 
                                    (self.time, tradedPrice, tradedQty, 
                                    counterparty, quote['tid']))
                    
                    transactionRecord = {'timestamp': self.time,
                                        'price': tradedPrice,
                                        'qty': tradedQty,
                                        'time': self.time}

                    currentParty = quote['tid']
                    delta_eth = tradedQty * tradedPrice
                    delta_bas = tradedQty

                    # bid means that I am willing to pay at max 0.01 ETH for 1 BAS.  
                    if side == 'bid':
                        transactionRecord['party1'] = [counterparty, 
                                                    'bid', 
                                                    headOrder.idNum]
                        transactionRecord['party2'] = [currentParty, 
                                                    'ask',
                                                    None]
                        
                        self.traderPool[currentParty].bas += delta_bas
                        self.traderPool[counterparty].bas -= delta_bas

                        self.traderPool[currentParty].eth -= delta_eth
                        self.traderPool[counterparty].eth += delta_eth
                        
                    else:
                        transactionRecord['party1'] = [counterparty, 
                                                    'ask', 
                                                    headOrder.idNum]
                        transactionRecord['party2'] = [currentParty, 
                                                    'bid',
                                                    None]

                        self.traderPool[currentParty].bas -= delta_bas
                        self.traderPool[counterparty].bas += delta_bas

                        self.traderPool[currentParty].eth += delta_eth
                        self.traderPool[counterparty].eth -= delta_eth

                    self.tape.append(transactionRecord)
                    trades.append(transactionRecord)
                return qtyToTrade, trades
            
            def processMarketOrder(self, quote, verbose):
                trades = []
                qtyToTrade = quote['qty']
                side = quote['side']
                if side == 'bid':
                    while qtyToTrade > 0 and self.asks: 
                        bestPriceAsks = self.asks.minPriceList()
                        qtyToTrade, newTrades = self.processOrderList('ask', 
                                                                        bestPriceAsks, 
                                                                        qtyToTrade, 
                                                                        quote, verbose)
                        trades += newTrades
                elif side == 'ask':
                    while qtyToTrade > 0 and self.bids: 
                        bestPriceBids = self.bids.maxPriceList()
                        qtyToTrade, newTrades = self.processOrderList('bid', 
                                                                        bestPriceBids, 
                                                                        qtyToTrade, 
                                                                        quote, verbose)
                        trades += newTrades
                else:
                    sys.exit('processMarketOrder() received neither "bid" nor "ask"')
                return trades
            
            def processLimitOrder(self, quote, fromData, verbose):
                orderInBook = None
                trades = []
                qtyToTrade = quote['qty']
                side = quote['side']
                price = quote['price']
                if side == 'bid':
                    while (self.asks and price >= self.asks.minPrice() and qtyToTrade > 0):
                        bestPriceAsks = self.asks.minPriceList()
                        qtyToTrade, newTrades = self.processOrderList('ask', 
                                                                    bestPriceAsks, 
                                                                    qtyToTrade, 
                                                                    quote, verbose)
                        trades += newTrades
                    # If volume remains, add to book
                    if qtyToTrade > 0:
                        if not fromData:
                            quote['idNum'] = self.nextQuoteID
                        quote['qty'] = qtyToTrade
                        self.bids.insertOrder(quote)
                        orderInBook = quote
                elif side == 'ask':
                    while (self.bids and price <= self.bids.maxPrice() and qtyToTrade > 0):
                        bestPriceBids = self.bids.maxPriceList()
                        qtyToTrade, newTrades = self.processOrderList('bid', 
                                                                    bestPriceBids, 
                                                                    qtyToTrade, 
                                                                    quote, verbose)
                        trades += newTrades
                    # If volume remains, add to book
                    if qtyToTrade > 0:
                        if not fromData:
                            quote['idNum'] = self.nextQuoteID
                        quote['qty'] = qtyToTrade
                        self.asks.insertOrder(quote)
                        orderInBook = quote
                else:
                    sys.exit('processLimitOrder() given neither bid nor ask')
                return trades, orderInBook

            def cancelOrder(self, side, idNum, time = None):
                if time:
                    self.time = time
                else:
                    self.updateTime()
                if side == 'bid':
                    if self.bids.orderExists(idNum):
                        self.bids.removeOrderById(idNum)
                elif side == 'ask':
                    if self.asks.orderExists(idNum):
                        self.asks.removeOrderById(idNum)
                else:
                    sys.exit('cancelOrder() given neither bid nor ask')
            
            def modifyOrder(self, idNum, orderUpdate, time=None):
                if time:
                    self.time = time
                else:
                    self.updateTime()
                side = orderUpdate['side']
                orderUpdate['idNum'] = idNum
                orderUpdate['timestamp'] = self.time
                if side == 'bid':
                    if self.bids.orderExists(orderUpdate['idNum']):
                        self.bids.updateOrder(orderUpdate)
                elif side == 'ask':
                    if self.asks.orderExists(orderUpdate['idNum']):
                        self.asks.updateOrder(orderUpdate)
                else:
                    sys.exit('modifyOrder() given neither bid nor ask')
            
            def getVolumeAtPrice(self, side, price):
                price = self.clipPrice(price)
                if side =='bid':
                    vol = 0
                    if self.bids.priceExists(price):
                        vol = self.bids.getPrice(price).volume
                    return vol
                elif side == 'ask':
                    vol = 0
                    if self.asks.priceExists(price):
                        vol = self.asks.getPrice(price).volume
                    return vol
                else:
                    sys.exit('getVolumeAtPrice() given neither bid nor ask')
            
            def getBestBid(self):
                return self.bids.maxPrice()
            def getWorstBid(self):
                return self.bids.minPrice()
            def getBestAsk(self):
                return self.asks.minPrice()
            def getWorstAsk(self):
                return self.asks.maxPrice()
            
            def tapeDump(self, fname, fmode, tmode):
                    dumpfile = open(fname, fmode)
                    for tapeitem in self.tape:
                        dumpfile.write('%s, %s, %s\n' % (tapeitem['time'], 
                                                        tapeitem['price'], 
                                                        tapeitem['qty']))
                    dumpfile.close()
                    if tmode == 'wipe':
                            self.tape = []
            
            def __str__(self):
                fileStr = StringIO()
                fileStr.write("------ Bids -------\n")
                if self.bids != None and len(self.bids) > 0:
                    for k, v in self.bids.priceTree.items(reverse=True):
                        fileStr.write('%s' % v)
                fileStr.write("\n------ Asks -------\n")
                if self.asks != None and len(self.asks) > 0:
                    for k, v in self.asks.priceTree.items():
                        fileStr.write('%s' % v)
                fileStr.write("\n------ Trades ------\n")
                if self.tape != None and len(self.tape) > 0:
                    num = 0
                    for entry in self.tape:
                        if num < 5:
                            fileStr.write(str(entry['qty']) + " @ " + 
                                        str(entry['price']) + 
                                        " (" + str(entry['timestamp']) + ")\n")
                            num += 1
                        else:
                            break
                fileStr.write("\n")
                return fileStr.getvalue()


        class OrderList(object):
            def __init__(self):
                self.headOrder = None
                self.tailOrder = None
                self.length = 0
                self.volume = 0    # Total share volume
                self.last = None
                
            def __len__(self):
                return self.length
            
            def __iter__(self):
                self.last = self.headOrder
                return self
            
            def next(self):
                if self.last == None:
                    raise StopIteration
                else:
                    returnVal = self.last
                    self.last = self.last.nextOrder
                    return returnVal
            
            def __next__(self):
                return self.next()

            def getHeadOrder(self):
                return self.headOrder
            
            def appendOrder(self, order):
                if len(self) == 0:
                    order.nextOrder = None
                    order.prevOrder = None
                    self.headOrder = order
                    self.tailOrder = order
                else:
                    order.prevOrder = self.tailOrder
                    order.nextOrder = None
                    self.tailOrder.nextOrder = order
                    self.tailOrder = order
                self.length += 1
                self.volume += order.qty
                
            def removeOrder(self, order):
                self.volume -= order.qty
                self.length -= 1
                if len(self) == 0:
                    return
                # Remove from list of orders
                nextOrder = order.nextOrder
                prevOrder = order.prevOrder
                if nextOrder != None and prevOrder != None:
                    nextOrder.prevOrder = prevOrder
                    prevOrder.nextOrder = nextOrder
                elif nextOrder != None:
                    nextOrder.prevOrder = None
                    self.headOrder = nextOrder
                elif prevOrder != None:
                    prevOrder.nextOrder = None
                    self.tailOrder = prevOrder
                    
            def moveTail(self, order):
                if order.prevOrder != None:
                    order.prevOrder.nextOrder = order.nextOrder
                else:
                    # Update the head order
                    self.headOrder = order.nextOrder
                order.nextOrder.prevOrder = order.prevOrder
                # Set the previous tail order's next order to this order
                self.tailOrder.nextOrder = order
                order.prevOrder = self.tailOrder
                self.tailOrder = order
                order.nextOrder = None
                
            def __str__(self):
                from io import StringIO
                file_str = StringIO()
                for order in self:
                    file_str.write("%s\n" % str(order))
                return file_str.getvalue()

        ##SIMULATOR

        class Trader: 
            def __init__(self, tid, protocol, market):
                self.tid = tid
                self.protocol = protocol
                self.market = market
                self.riskRatio = 0.5
                self.eth = 10
                self.bas = 1000
                self.bondsLiquidated = 0
                
            def liquidate(self, amount):
                self.bas += amount
                self.bondsLiquidated += amount
                
            def get_price(self, side, base_price):        
                # Set price around BASE_PRICE
                price = normal(base_price, PRICE_NOISE)
                if side == 'bid':
                    price -= (base_price * BASE_SPREAD) 
                else:
                    price += (base_price * BASE_SPREAD) 
                return clamp_bas_price(price)
                
            def get_qty(self):
                qty_mu = self.riskRatio
                qty_sigma = qty_mu * 0.1
                qty = normal(qty_mu, qty_sigma) * self.bas
                return clamp_bas_qty(qty)
                
            def getIdealValue(self):
                return self.eth * 100 + self.bas

            def marketStep(self):
                return []
            
        '''
            IdealTrader buys/sells according to market demand. 
            Sets prices to be around the ideal exchange rate ~ 0.01.
        '''
        class IdealTrader(Trader):
            def __init__(self, tid, protocol, market):
                super().__init__(tid, protocol, market)
                self.bas = int(1e5) # $100,000 in BASIS 
                self.riskRatio = 0.05
                
            def marketStep(self):
                # Randomly select bid / ask based on market demand
                side = ['bid', 'ask'][biased_coin(0.5)]
                
                # Set Quantity around portfolio ratio 
                qty = self.get_qty()

                if qty <= 0:
                    return []
                
                # Set price around BASE_PRICE
                price = self.get_price(side, self.market.usd_eth)
                
                order = {'type': 'limit', 'price': price, 'tid': self.tid, 'side': side, 'qty': qty}
                return [order]
            
        class AverageTrader(Trader): 
            def __init__(self, tid, protocol, market):
                super().__init__(tid, protocol, market)
                self.riskRatio = 0.05
                self.bas = int(1e4)
                
            def marketStep(self):
                # Set Quantity around portfolio ratio 
                qty = self.get_qty()
                
                if qty <= 0:
                    return []
                
                # Randomly select bid / ask based on market demand
                side = ['ask', 'bid'][biased_coin(self.market.demandRatio)]
                
                # Try to see if need for BAS can be satisfied with liquidated bonds
                if side == 'bid' and self.bondsLiquidated:
                    if self.bondsLiquidated >= qty:
                        self.bondsLiquidated -= qty
                        return []
                    else:
                        qty -= self.bondsLiquidated
                        self.bondsLiquidated = 0
                
                # If there is high confidence, then buy bonds in the auction.
                if side == 'ask' and biased_coin(self.market.demandRatio) and self.protocol.bondsForAuction:
                    # Buy the bonds for a price 
                    price = randint(90, 99) * 0.01 # Gets the price the person is willing to pay for the bonds
                    qty = min(qty, self.protocol.bondsForAuction)
                    qty = min(qty, self.bas / price)
                    self.protocol.issueBonds(self.tid, qty)
                    burntBasis = price * qty
                    self.bas -= burntBasis
                    self.protocol.totalSupply -= burntBasis
                    return []
                
                # Set price around BASE_PRICE
                price = self.get_price(side, self.market.getIdealETHValue())
                
                order = {'type': 'limit', 'price': price, 'tid': self.tid, 'side': side, 'qty': qty}
                return [order]

            
        class InvestorTrader(Trader): 
            def __init__(self, tid, protocol, market):
                super().__init__(tid, protocol, market)
                self.riskRatio = 0.001
                self.bas = int(1e8)
                self.threshold = BASIC_TRADER_THRESHOLD
                self.eth = 1000

            def marketStep(self):
                # Set Quantity around portfolio ratio 
                qty = self.get_qty()
                
                if qty <= 0:
                    return []
                
                # Randomly select bid / ask based on market demand
                side = ['ask', 'bid'][biased_coin(self.market.demandRatio)]
                
                # Try to see if need for BAS can be satisfied with liquidated bonds
                if side == 'bid' and self.bondsLiquidated:
                    if self.bondsLiquidated >= qty:
                        self.bondsLiquidated -= qty
                        return []
                    else:
                        qty -= self.bondsLiquidated
                        self.bondsLiquidated = 0
                # If there is high confidence, then buy bonds in the auction.
                if side == 'ask' and biased_coin(self.market.demandRatio) and self.protocol.bondsForAuction:
                    # Buy the bonds for a price 
                    price = randint(90, 99) * 0.01 # Gets the price the person is willing to pay for the bonds
                    qty = min(qty, self.protocol.bondsForAuction)
                    qty = min(qty, self.bas / price)
                    self.protocol.issueBonds(self.tid, qty)
                    burntBasis = price * qty
                    self.bas -= burntBasis
                    self.protocol.totalSupply -= burntBasis
                    return []
                
                # Set price around BASE_PRICE
                price = self.get_price(side, self.market.getIdealETHValue())
                
                order = {'type': 'limit', 'price': price, 'tid': self.tid, 'side': side, 'qty': qty}
                return [order]

            
        class TrendMaker(Trader):
            pass

        class BasicTrader(Trader): 
            def __init__(self, tid, protocol, market):
                super().__init__(tid, protocol, market)
                self.riskRatio = 0.05
                self.threshold = BASIC_TRADER_THRESHOLD
                self.bas = int(1e4)
                
            def marketStep(self):
                # Set Quantity around portfolio ratio 
                qty = self.get_qty()
                
                if qty <= 0:
                    return []
                
                # Randomly select bid / ask based on market demand
                if self.market.getCurrentUSDValue() <= 1.0 - self.threshold:
                    side = 'bid'
                elif self.market.getCurrentUSDValue() >= 1.0 + self.threshold:
                    side = 'ask'
                else:
                    return []
                
                if self.market.demandRatio < 0.2 and side == 'bid':
                    return []
                
                if self.market.demandRatio > 0.8 and side == 'ask':
                    return []
                
                # Set price around BASE_PRICE
                price = self.get_price(side, self.market.getIdealETHValue())
                
                order1 = {'type': 'limit', 'price': price, 'tid': self.tid, 'side': side, 'qty': qty}
                return [order1]

                # other_side = 'bid' if side == 'ask' else 'ask'
                # order2 = {'type': 'limit', 'price': self.market.usd_eth, 'tid': self.tid, 'side': other_side, 'qty': qty}
                # return [order1, order2]

        trader_dict = {'IdealTrader': IdealTrader, 'AverageTrader': AverageTrader, 'TrendMaker': TrendMaker, 
                    'BasicTrader': BasicTrader, 'InvestorTrader': InvestorTrader}


        # Implement TrendMaker, ShareTokens, ShareHolderTrader
        def createTraderPool(protocol, market, demographics):
            traderPool = {}
            uniqTID = 1
            for trader_type, number in demographics.items():
                trader_class = trader_dict[trader_type]
                for i in range(number):
                    trader = trader_class(uniqTID, protocol, market)
                    traderPool[uniqTID] = trader
                    uniqTID += 1
            return traderPool

        class BasisBond: 
            def __init__(self, tid, timestamp, amount, expiry):
                self.tid = tid
                self.timestamp = int(timestamp)
                self.expirytime = self.timestamp + expiry
                self.amount = amount

        class Protocol:
            def __init__(self, totalSupply):
                self.totalSupply = totalSupply
                self.market = None
                
            def update(self):
                pass
                
        class BasisProtocol(Protocol):
            
            def __init__(self, totalSupply, market):
                super().__init__(totalSupply)
                self.market = market
                self.bond_expiry = BOND_EXPIRY # 5 year expiry
                self.bondsForAuction = 0
                self.bondQueue = deque()
                self.bondQueueLength = 0
                self.delay = BOND_DELAY # In Steps
                self.lastAuction = 0 # Last aucion
                self.currentStep = 0
                
            def issueBonds(self, tid, amount):
                self.bondQueue.append(BasisBond(tid, time.time(), amount, self.bond_expiry))
                self.bondsForAuction -= amount
                self.bondQueueLength += amount
                
                # Basis are burnt outside of this code 
                
            def update(self):
                price = self.market.getCurrentUSDValue()
                self.currentStep += 1
                
                LOWER, UPPER = BOND_RANGE
                
                if self.currentStep < self.lastAuction + self.delay:
                    return

                # ISSUE bonds
                if price < LOWER:
                    bondsToCreate = (1. - price) * self.market.getCirculation() 
                    self.bondsForAuction += bondsToCreate
                    self.lastAuction = self.currentStep
                    
                elif price > UPPER:
                    basisToCreate = (price - 1.) * self.market.getCirculation() 
                    self.lastAuction = self.currentStep
                    
                    while len(self.bondQueue) and basisToCreate:
                        head = self.bondQueue.popleft()
                        if head.amount > basisToCreate:
                            self.market.traderPool[head.tid].liquidate(head.amount)
                            head.amount -= basisToCreate
                            basisToCreate = 0
                            self.bondQueue.appendleft(head)
                            self.bondQueueLength -= basisToCreate
                        else:
                            self.market.traderPool[head.tid].liquidate(head.amount)
                            basisToCreate -= head.amount
                            self.bondQueueLength -= head.amount
                            
                    if basisToCreate > 0:
                        # Distribute to shareholders
                        pass
                    

        class Market:
            def __init__(self):
                self.demandRatio = 0.5 # in [0, 1]
                
                # ETH Trades
                self.usd_eth = 0.01
                
                self.orderbook = OrderBook(tick_size=0.0001)
                self.traderPool = {}
                
                self.prices = defaultdict(list)
                self.prices['MAday'] = [0]
                self.protocol = None
                self.marketSpeed = MARKET_SPEED
                
                self.askVolume = 0
                self.bidVolume = 0
                self.totalVolume = 0
                self.volMAvel = 1. / VOL_MA_STEPS
                self.priceMAvel = 1. / PRICE_MA_STEPS
                
            def setTraderPool(self, traderPool):
                self.traderPool = traderPool
                
                if self.protocol:
                    basis = 0
                    for trader in traderPool.values():
                        basis += trader.bas
                    self.protocol.totalSupply = basis
                
                self.orderbook.setTraderPool(traderPool)
                
            def getIdealETHValue(self):
                return self.marketSpeed * self.usd_eth + (1 - self.marketSpeed) * self.getCurrentETHValue()
                
            def getCurrentUSDValue(self, func_type='wavg_fair'):
                return self.getCurrentETHValue(func_type) / self.usd_eth
                
            ''' Returns the value of BASIS in USD '''
            def getCurrentETHValue(self, func_type='wavg_fair'):
                def avg_bidask():
                    return (self.orderbook.getBestBid() + self.orderbook.getBestAsk()) / 2
                
                def wavg_bidask():
                    bid_price, ask_price = self.orderbook.getBestBid(), self.orderbook.getBestAsk()
                    bid_vol = self.orderbook.getVolumeAtPrice('bid', bid_price)
                    ask_vol = self.orderbook.getVolumeAtPrice('ask', ask_price)
                    total_vol = bid_vol + ask_vol
                    return (bid_price * ask_vol + ask_price * bid_vol) / total_vol
                
                if self.orderbook.getBestBid() is None:
                    if self.orderbook.getBestAsk() is not None: 
                        return self.orderbook.getBestAsk() # ask, not bid
                    else:
                        return self.usd_eth # not ask, not bid
                elif self.orderbook.getBestAsk() is None:
                    return self.orderbook.getBestBid() # not ask, bid
                
                func_list = {'avg_fair': avg_bidask, 'wavg_fair': wavg_bidask}
                
                return func_list[func_type]()
                
            def setProtocol(self, protocol):
                self.protocol = protocol
                
            def updateDemandRatio(self, factor):
                self.demandRatio *= factor
                self.demandRatio = np.clip(self.demandRatio, 0.1, 1.0)
            
            def getCirculation(self):
                circulation = 0
                for trader in self.traderPool.values():
                    if isinstance(trader, InvestorTrader):
                        continue
                    circulation += trader.bas
                return circulation

            def getMAprice(self):
                return self.prices['MAday'][-1]
                
            def updateDemand(self):
                # MAprice returns the bas_usd price
                bas_eth = self.getMAprice() * self.usd_eth
                usd_eth = self.usd_eth
                delta = 0
                
                # Demand varies on the price
                if bas_eth < usd_eth and self.demandRatio < 0.8:
                    delta = (usd_eth - bas_eth) / usd_eth
                    self.updateDemandRatio(1 + delta * PRICE_SCALE)
                elif bas_eth > usd_eth and self.demandRatio > 0.2:   
                    delta = (bas_eth - usd_eth) / usd_eth
                    self.updateDemandRatio(1 - delta * PRICE_SCALE)
                    
                # Demand based on variation
                var = 1e2 * ((usd_eth - bas_eth) / usd_eth) ** 2
                
                if var <= 1e-2 and self.demandRatio < 0.6: # 1 cent 
                    self.updateDemandRatio(1 + VAR_SCALE)
                else:
                    self.updateDemandRatio(1 - var * VAR_SCALE)
                
            def processOrder(self, quote):
                trades, idNum = self.orderbook.processOrder(quote, False, False)
                
                volumeTraded = sum([trade['qty'] for trade in trades])
                askVolDelta, bidVolDelta = 0, 0
                if quote['side'] == 'bid':
                    askVolDelta += volumeTraded
                if quote['side'] == 'ask':
                    bidVolDelta += volumeTraded

                self.bidVolume = self.bidVolume * (1 - self.volMAvel) + bidVolDelta * self.volMAvel
                self.askVolume = self.askVolume * (1 - self.volMAvel) + askVolDelta * self.volMAvel
                self.totalVolume = self.bidVolume + self.askVolume
                
                # Calculates and saves the prices
                for func in ['avg_fair', 'wavg_fair']:
                    self.prices[func].append(self.getCurrentUSDValue(func))
                    
                maPrice = (self.prices['MAday'][-1] * (1 - self.priceMAvel) + 
                        self.getCurrentUSDValue('wavg_fair') * self.priceMAvel)
                
                self.prices['MAday'].append(maPrice)
                    
                # Updates the Demand Ratio and Protocol (in case needs to react to price changes)
                self.updateDemand()
                    
                if self.protocol is not None:
                    self.protocol.update()
                    
                return trades, idNum

        def bin_data(data, bin_size):
            valid_length = (data.shape[0] // bin_size) * bin_size
            data = data[:valid_length]
            N = data.shape[0]
            binned = np.zeros(N // bin_size)
            for k in range(0, N, bin_size):
                binned[k // bin_size] = data[k : k + bin_size].mean()
            return binned

        def compute_metrics(data, ideal): 
            diff = data - ideal
            l1 = float(np.mean(np.abs(diff)))
            l2 = float(np.mean(np.square(diff)))
            linf = float(np.max(np.abs(diff)))

            print ('L-1 Dev: %.5f' % l1)
            print ('L-2 Dev: %.5f' % l2)
            print ('L-inf Dev: %.5f' % linf)

        def plot_prices(market, price_func, bin_size=50, warmup=100, ideal_dev=0.1, title=''): 
            data = np.array(market.prices[price_func])[warmup:]
            binned = bin_data(data, bin_size)
            
            ideal = np.ones(binned.shape)

            compute_metrics(binned, ideal)
            # fig = go.Figure()
            # fig.add_trace(go.Scatter(binned,
            #                     mode='lines',
            #                     name='lines'))
            # px.line(ideal)
            # plt.plot(ideal - ideal_dev)
            # plt.plot(ideal + ideal_dev)
            # fig = px.line(y=[binned, ideal,ideal + ideal_dev, ideal - ideal_dev], title=title)
            
            fig =go.Figure()
            fig.add_trace(go.Scatter( y=binned,
                                mode='lines',
                                name='1 BAS'))
            fig.add_trace(go.Scatter( y=ideal,
                    mode='lines',
                    name='1 USD'))
            fig.add_trace(go.Scatter( y=ideal + ideal_dev,
                                mode='lines',
                                name='Upper treshold'))
            fig.add_trace(go.Scatter( y=ideal - ideal_dev,
                                mode='lines', name='Lower treshold'))
            fig.update_layout(title_text=title)
            fig.update_yaxes(range=[0.5, 1.5])
        #     plt.plot(market.prices['MAday'], 'y')
            # plt.ylim(1.0 - ideal_dev * 5, 1.0 + ideal_dev * 5)
            # plt.title(title)
            # plt.ylabel('USD price')
            # plt.legend()
            return fig

        market = Market()
        basis = BasisProtocol(int(1e7), market)
        market.protocol = basis
        traderPool = createTraderPool(basis, market, trader_demographics)
        market.setTraderPool(traderPool)

        cur_time = 0
        market.usd_eth = 1 / get_eth_price(0)

        trackers = {'usd_eth': [], 'bond_q_len': [], 'demand_ratio': [], 'ask_volume': [],
                    'bid_volume': [], 'total_volume': [], 'circulation': []}

        def track():
            trackers['usd_eth'].append(market.usd_eth)
            trackers['bond_q_len'].append(basis.bondQueueLength)
            trackers['demand_ratio'].append(market.demandRatio)
            trackers['ask_volume'].append(market.askVolume)
            trackers['bid_volume'].append(market.bidVolume)
            trackers['total_volume'].append(market.totalVolume)
            trackers['circulation'].append(market.getCirculation())



        NUM_TRADERS = trader_demographics['IdealTrader'] # We initially set it up with randomTraders

        for i in range(NUM_ORDERS_INIT):
            market.usd_eth = 1. / get_eth_price(cur_time) 
            
            tid = randint(1, NUM_TRADERS)
            orders = traderPool[tid].marketStep()
            for order in orders:
                market.processOrder(order)
            cur_time += 1
        market.demandRatio = 0.5
    
        figure1 = plot_prices(market, 'wavg_fair', warmup=100, ideal_dev=0.1, bin_size=50, title='Initial Warmup')
        


        NUM_TRADERS = trader_demographics['AverageTrader'] + trader_demographics['BasicTrader']  
        OFFSET_TRADERS = trader_demographics['IdealTrader']

        for i in range(NUM_ORDERS_LIVE):
            market.usd_eth = 1 / get_eth_price(cur_time) 
            if i % TRACK_FREQ == 0:
                track()
            
            tid = randint(OFFSET_TRADERS + 1, OFFSET_TRADERS + NUM_TRADERS)
            orders = traderPool[tid].marketStep()
            for order in orders:
                market.processOrder(order)    
            cur_time += 1
        figure = plot_prices(market, 'MAday', bin_size=50, warmup=NUM_ORDERS_INIT, title='BAS vs USD')


        NUM_TRADERS1 = trader_demographics['AverageTrader'] + trader_demographics['BasicTrader']+  trader_demographics['InvestorTrader']
        OFFSET_TRADERS = trader_demographics['IdealTrader']

        for i in range(NUM_ORDERS_LIVE):
            market.usd_eth = 1 / get_eth_price(cur_time) 
            if i % TRACK_FREQ == 0:
                track()
            
            tid = randint(OFFSET_TRADERS + 1, OFFSET_TRADERS + NUM_TRADERS1)
            orders = traderPool[tid].marketStep()
            for order in orders:
                market.processOrder(order)    
            cur_time += 1
        figure2 = plot_prices(market, 'MAday', bin_size=50, warmup=NUM_ORDERS_INIT, title='BAS vs USD (with Investor Trader)')
        

        TRUNCATE = (NUM_ORDERS_INIT) // TRACK_FREQ
        df = trackers


        return df, figure, figure1, figure2 

@app.callback(Output('grafik2', 'figure'),Output('grafik3', 'figure'),Output('grafik4', 'figure'),Output('grafik5', 'figure'), Output('grafik6', 'figure'), Input('data', 'data'))
def plot4(tracker):

    df = pd.DataFrame(tracker)#tracker1 = tracker
    df1 = {}
    df2 = {}
    df3 = {}
    df4 = {}
    df5 = {}
    df6 = {}

    if not df.empty:
        df1 = df['ask_volume']
        df2 = df['bid_volume']
        df3 = df['total_volume']
        df4 = df['usd_eth']
        df5 = df['bond_q_len']
        df6 = df['demand_ratio']
        df7 = df['circulation']
    
    

    figure1 = px.line(df,  y=['ask_volume','bid_volume', 'total_volume'], title='Average Trade Volume')
    #figure1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 1)'})
    figure2 = px.line(df,  y=['usd_eth'], title='USD - ETH')
    #figure2.update_layout(bgcolor = 'black')
    figure3 = px.line(df,  y=['bond_q_len'], title='Bond Queue Length')
    figure4 = px.line(df,  y=['circulation'], title='Coin Circulation')
    figure5 = px.line(df,  y=['demand_ratio'], title='Demand Ratio (θ)')

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(df1,
    #                 mode='lines+markers',
    #                 name='lines+markers'))
    # fig.add_trace(go.Scatter(df2,
    #                 mode='lines+markers',
    #                 name='lines+markers')) 
    # figure1 = px.line(df1)
    # figure2 = px.line(df2)
    return  figure1, figure2, figure3, figure4, figure5