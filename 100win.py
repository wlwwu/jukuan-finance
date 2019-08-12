##513100 纳指

def initialize(context):
    g.cntLost = 0
    g.cntProfit = 0
    g.lost = 0
    g.profit = 0
    

    
def getStockPrice(stock, interval):
    h = attribute_history(stock, interval, unit='1d', fields=('close'), skip_paused=True)
    return (h['close'].values[0],h['close'].values[-1],h['close'].mean())


def calPosition(context):
    return context.portfolio.cash


#记录每次盈亏
def calProfitLost(context,stock, price):
    if(context.portfolio.positions[stock].avg_cost < price):
        g.cntProfit = g.cntProfit + 1
        g.profit = g.profit + (price - context.portfolio.positions[stock].avg_cost)*context.portfolio.positions[stock].total_amount
    else:
        g.cntLost = g.cntLost + 1
        g.lost = g.lost - (price - context.portfolio.positions[stock].avg_cost)*context.portfolio.positions[stock].total_amount

def logDate(context, stock, isbuy):
    if isbuy == True:
        print("%s   %s      buy"%(context.current_dt.strftime("F"), stock))
    else:
        print("%s   %s      sell"%(context.current_dt.strftime("F"), stock))

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context,data):
    interval = 21
    etf2 = '518880.XSHG'#黄金
    etf8 = '159915.XSHE'#创业板
    etf10 = '513100.XSHG'#纳指
    etf20 = '511800.XSHG'#货币
    etf30 = '510880.XSHG'#红利etf
    # etf40 = '159928.XSHE'#消费
    # etf50 = '511800.XSHG'
    etf_list = [etf2,etf8,etf10,etf30]
    hs2,cp2,av2 = getStockPrice(etf2, interval)
    hs8,cp8,av8 = getStockPrice(etf8, interval)
    hs10,cp10,av10 = getStockPrice(etf10, interval)
    # hs40,cp40,av40 = getStockPrice(etf40, interval)
    hs30,cp30,av30 = getStockPrice(etf30, interval)
    # hs50,cp50,av50 = getStockPrice(etf50, interval)
    hs2Increase = (cp2 - hs2) / hs2;
    hs8Increase = (cp8 - hs8) / hs8;
    hs10Increase = (cp10 - hs10) / hs10;
    # hs40Increase = (cp40 - hs40) / hs40;
    hs30Increase = (cp30 - hs30) / hs30;
    # hs50Increase = (cp50 - hs50) / hs50;
    # print(cp40)
    # print(hs40)
    print('hs2Increase-黄金:' + str(hs2Increase))
    print('hs8Increase-创业板:' + str(hs8Increase))
    print('hs10Increase-纳指:' + str(hs10Increase))
    # print('hs20Increase-货币:' + str(hs20Increase))
    print('hs30Increase-红利etf:' + str(hs30Increase))
    # print('hs40Increase-消费:' + str(hs40Increase))
    daily_data = {}
    daily_data[etf2] = hs2Increase
    daily_data[etf8] = hs8Increase
    daily_data[etf10] = hs10Increase
    # daily_data[etf40] = hs40Increase
    daily_data[etf30] = hs30Increase
    # daily_data[etf50] = hs50Increase
    cp_data = {}
    cp_data[etf2] = cp2
    cp_data[etf8] = cp8
    cp_data[etf10] = cp10
    # cp_data[etf40] = cp40
    cp_data[etf30] = cp30
    # cp_data[etf50] = cp50
    av_data = {}
    av_data[etf2] = av2
    av_data[etf8] = av8
    av_data[etf10] = av10
    # av_data[etf40] = av40
    av_data[etf30] = av30
    # av_data[etf50] = av50
    max_etf = max(daily_data, key=daily_data.get)
    print(cp_data)
    print(av_data)
    print('最大动量的ETF：' + max_etf)
    # if cp_data[max_etf] > av_data[max_etf]:
    if daily_data[max_etf] > 0:
       etf_list.remove(max_etf)
       for etf in etf_list:
           if context.portfolio.positions[etf].total_amount > 0:
                calProfitLost(context,etf, data[etf].close)
                order_target_value(etf, 0)
                logDate(context, etf, False)
       if context.portfolio.positions[max_etf].total_amount > 0:
           return 
       else:
            print("购买最大动量的etf")
            target_order = round(calPosition(context))
            order_target_value(etf20,0.1*target_order)
            order_target_value(max_etf,0.9*target_order)    
    else:
        for etf in etf_list:
            if context.portfolio.positions[etf].total_amount > 0:
               calProfitLost(context,etf, data[etf].close)
               order_target_value(etf, 0)    
               logDate(context, etf, False)
        print("购买货币基金")
        target_order = round(calPosition(context))
        order_target_value(etf20,target_order) 
