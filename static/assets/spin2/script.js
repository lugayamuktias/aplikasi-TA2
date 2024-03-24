// DATA

(() => {
})

var tokenspin = data_token.length;
if(tokenspin <= 0){
    $('#push').remove()
    $('#istukar').remove()
}

$('#isbuttontukar').prop("disabled", true)

$('#push').on('click',function () {
    var audio = $("#wheel")[0];
    audio.play();
})

$('#total-token').on('change',function () {
    
    if(this.value >= tokenspin){
        
        if(this.value >= 5){
            
            if(this.value > 5){
                if(tokenspin < this.value){
                    if(this.value > tokenspin){
                        if(tokenspin < this.value){

                        }else{
                            tokenspin = 5
                        }
                    }else{
                        tokenspin = tokenspin
                    }
                }else{
                    tokenspin = 5
                }
                $('#total-token').val(tokenspin)
            }else{
                $('#total-token').val(tokenspin)
            }            

        }
        
        $('#push').prop("disabled", false)
    }else if(this.value <= tokenspin){
        
        if(this.value >= 5){
            if(this.value > 5){
                if(tokenspin < this.value){
                    
                    tokenspin = tokenspin
                }else{
                    tokenspin = 5
                }
            }else{
                tokenspin = 5
            }
            
            $('#total-token').val(tokenspin)
        }

        
        $('#push').prop("disabled", false)
    }else if(this.value <= 0){
        $('#push').prop("disabled", true)
    }else if(this.value > 0){
        $('#push').prop("disabled", false)
    }

})
const rawData = [];
var data_1 = data_voucer
var data_2 = data_voucer
var n_data_voucer =  [...data_1, ...data_2];
for (let i = 0; i < n_data_voucer.length; i++){
  const element = n_data_voucer[i];
  
  rawData.push({
      "cmc_rank": element.id_voucher,
      "ticker": element.nm_voucher.replace('Voucher',''),
      "name": element.nm_voucher,
      "code": element.kd_voucher,
      // "full_name": "Revain (R)",
      // "supply": 484450000,
      // "price": 0.102341,
      // "vladimir_coins": 48445,
      // "vladimir_costs": 4958,
      // "coins_per_pers": 0.062992
  })
}
let top100 = rawData
// DOM ELEMENTS
const box = document.querySelector('.difficulty__buttons');
const buttons = Array.from(document.getElementsByClassName('difficulty__button'));
const modal = document.getElementById('modal');
const closeBtn = document.querySelector('.closeBtn');
let selection = top100.length;
// let selection = document.querySelector('.current').value;


// DATA
let data = getData(selection);

// let top100 = [
//   {
//     "cmc_rank": 1,
//     "ticker": "BTC",
//     "name": "Bitcoin",
//     "full_name": "Bitcoin (BTC)",
//     "supply": 21000000,
//     "price": 7066.424046,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 14839490,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 2,
//     "ticker": "ETH",
//     "name": "Ethereum",
//     "full_name": "Ethereum (ETH)",
//     "supply": 106048732.44,
//     "price": 188.768102,
//     "vladimir_coins": 10605,
//     "vladimir_costs": 2001862,
//     "coins_per_pers": 0.013789
//   },
//   {
//     "cmc_rank": 3,
//     "ticker": "XRP",
//     "name": "XRP",
//     "full_name": "XRP (XRP)",
//     "supply": 100000000000,
//     "price": 0.317099,
//     "vladimir_coins": 10000000,
//     "vladimir_costs": 3170991,
//     "coins_per_pers": 13.002802
//   },
//   {
//     "cmc_rank": 4,
//     "ticker": "BCH",
//     "name": "Bitcoin Cash",
//     "full_name": "Bitcoin Cash (BCH)",
//     "supply": 21000000,
//     "price": 354.063884,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 743534,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 5,
//     "ticker": "LTC",
//     "name": "Litecoin",
//     "full_name": "Litecoin (LTC)",
//     "supply": 84000000,
//     "price": 85.78854,
//     "vladimir_coins": 8400,
//     "vladimir_costs": 720624,
//     "coins_per_pers": 0.010922
//   },
//   {
//     "cmc_rank": 6,
//     "ticker": "EOS",
//     "name": "EOS",
//     "full_name": "EOS (EOS)",
//     "supply": 1011411073.56,
//     "price": 5.36571,
//     "vladimir_coins": 101141,
//     "vladimir_costs": 542694,
//     "coins_per_pers": 0.131512
//   },
//   {
//     "cmc_rank": 7,
//     "ticker": "BNB",
//     "name": "Binance Coin",
//     "full_name": "Binance Coin (BNB)",
//     "supply": 189175490.24,
//     "price": 23.386562,
//     "vladimir_coins": 18918,
//     "vladimir_costs": 442416,
//     "coins_per_pers": 0.024598
//   },
//   {
//     "cmc_rank": 8,
//     "ticker": "USDT",
//     "name": "Tether",
//     "full_name": "Tether (USDT)",
//     "supply": 3220057493.36,
//     "price": 0.99718,
//     "vladimir_coins": 322006,
//     "vladimir_costs": 321098,
//     "coins_per_pers": 0.418698
//   },
//   {
//     "cmc_rank": 9,
//     "ticker": "XLM",
//     "name": "Stellar",
//     "full_name": "Stellar (XLM)",
//     "supply": 104962402033.84,
//     "price": 0.100675,
//     "vladimir_coins": 10496240,
//     "vladimir_costs": 1056707,
//     "coins_per_pers": 13.648053
//   },
//   {
//     "cmc_rank": 10,
//     "ticker": "ADA",
//     "name": "Cardano",
//     "full_name": "Cardano (ADA)",
//     "supply": 45000000000,
//     "price": 0.071899,
//     "vladimir_coins": 4500000,
//     "vladimir_costs": 323546,
//     "coins_per_pers": 5.851261
//   },
//   {
//     "cmc_rank": 11,
//     "ticker": "TRX",
//     "name": "TRON",
//     "full_name": "TRON (TRX)",
//     "supply": 99281283754.3,
//     "price": 0.024411,
//     "vladimir_coins": 9928128,
//     "vladimir_costs": 242355,
//     "coins_per_pers": 12.909349
//   },
//   {
//     "cmc_rank": 12,
//     "ticker": "XMR",
//     "name": "Monero",
//     "full_name": "Monero (XMR)",
//     "supply": 16976901.8,
//     "price": 75.479992,
//     "vladimir_coins": 1698,
//     "vladimir_costs": 128142,
//     "coins_per_pers": 0.002207
//   },
//   {
//     "cmc_rank": 13,
//     "ticker": "DASH",
//     "name": "Dash",
//     "full_name": "Dash (DASH)",
//     "supply": 18900000,
//     "price": 129.787914,
//     "vladimir_coins": 1890,
//     "vladimir_costs": 245299,
//     "coins_per_pers": 0.002458
//   },
//   {
//     "cmc_rank": 14,
//     "ticker": "BSV",
//     "name": "Bitcoin SV",
//     "full_name": "Bitcoin SV (BSV)",
//     "supply": 21000000,
//     "price": 57.376014,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 120490,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 15,
//     "ticker": "MIOTA",
//     "name": "IOTA",
//     "full_name": "IOTA (MIOTA)",
//     "supply": 2779530283,
//     "price": 0.31143,
//     "vladimir_coins": 277953,
//     "vladimir_costs": 86563,
//     "coins_per_pers": 0.361417
//   },
//   {
//     "cmc_rank": 16,
//     "ticker": "XTZ",
//     "name": "Tezos",
//     "full_name": "Tezos (XTZ)",
//     "supply": 794001681.87,
//     "price": 1.246603,
//     "vladimir_coins": 79400,
//     "vladimir_costs": 98980,
//     "coins_per_pers": 0.103242
//   },
//   {
//     "cmc_rank": 17,
//     "ticker": "ATOM",
//     "name": "Cosmos",
//     "full_name": "Cosmos (ATOM)",
//     "supply": 237928230.82,
//     "price": 4.13307,
//     "vladimir_coins": 23793,
//     "vladimir_costs": 98337,
//     "coins_per_pers": 0.030937
//   },
//   {
//     "cmc_rank": 18,
//     "ticker": "ETC",
//     "name": "Ethereum Classic",
//     "full_name": "Ethereum Classic (ETC)",
//     "supply": 210000000,
//     "price": 5.939436,
//     "vladimir_coins": 21000,
//     "vladimir_costs": 124728,
//     "coins_per_pers": 0.027306
//   },
//   {
//     "cmc_rank": 19,
//     "ticker": "NEO",
//     "name": "NEO",
//     "full_name": "NEO (NEO)",
//     "supply": 100000000,
//     "price": 9.467467,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 94675,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 20,
//     "ticker": "ONT",
//     "name": "Ontology",
//     "full_name": "Ontology (ONT)",
//     "supply": 1000000000,
//     "price": 1.210624,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 121062,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 21,
//     "ticker": "MKR",
//     "name": "Maker",
//     "full_name": "Maker (MKR)",
//     "supply": 1000000,
//     "price": 567.849449,
//     "vladimir_coins": 100,
//     "vladimir_costs": 56785,
//     "coins_per_pers": 0.00013
//   },
//   {
//     "cmc_rank": 22,
//     "ticker": "XEM",
//     "name": "NEM",
//     "full_name": "NEM (XEM)",
//     "supply": 8999999999,
//     "price": 0.0564,
//     "vladimir_coins": 900000,
//     "vladimir_costs": 50760,
//     "coins_per_pers": 1.170252
//   },
//   {
//     "cmc_rank": 23,
//     "ticker": "BAT",
//     "name": "Basic Attention Token",
//     "full_name": "Basic Attention Token (BAT)",
//     "supply": 1500000000,
//     "price": 0.361392,
//     "vladimir_coins": 150000,
//     "vladimir_costs": 54209,
//     "coins_per_pers": 0.195042
//   },
//   {
//     "cmc_rank": 24,
//     "ticker": "ZEC",
//     "name": "Zcash",
//     "full_name": "Zcash (ZEC)",
//     "supply": 6521856.25,
//     "price": 61.336609,
//     "vladimir_coins": 652,
//     "vladimir_costs": 40003,
//     "coins_per_pers": 0.000848
//   },
//   {
//     "cmc_rank": 25,
//     "ticker": "BTG",
//     "name": "Bitcoin Gold",
//     "full_name": "Bitcoin Gold (BTG)",
//     "supply": 21000000,
//     "price": 21.710529,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 45592,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 26,
//     "ticker": "CRO",
//     "name": "Crypto.com Chain",
//     "full_name": "Crypto.com Chain (CRO)",
//     "supply": 100000000000,
//     "price": 0.065307,
//     "vladimir_coins": 10000000,
//     "vladimir_costs": 653068,
//     "coins_per_pers": 13.002802
//   },
//   {
//     "cmc_rank": 27,
//     "ticker": "VET",
//     "name": "VeChain",
//     "full_name": "VeChain (VET)",
//     "supply": 86712634466,
//     "price": 0.006317,
//     "vladimir_coins": 8671263,
//     "vladimir_costs": 54774,
//     "coins_per_pers": 11.275072
//   },
//   {
//     "cmc_rank": 28,
//     "ticker": "USDC",
//     "name": "USD Coin",
//     "full_name": "USD Coin (USDC)",
//     "supply": 327797776.94,
//     "price": 0.998419,
//     "vladimir_coins": 32780,
//     "vladimir_costs": 32728,
//     "coins_per_pers": 0.042623
//   },
//   {
//     "cmc_rank": 29,
//     "ticker": "DOGE",
//     "name": "Dogecoin",
//     "full_name": "Dogecoin (DOGE)",
//     "supply": 119475615248.98,
//     "price": 0.002696,
//     "vladimir_coins": 11947562,
//     "vladimir_costs": 32209,
//     "coins_per_pers": 15.535178
//   },
//   {
//     "cmc_rank": 30,
//     "ticker": "DCR",
//     "name": "Decred",
//     "full_name": "Decred (DCR)",
//     "supply": 21000000,
//     "price": 27.50225,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 57755,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 31,
//     "ticker": "WAVES",
//     "name": "Waves",
//     "full_name": "Waves (WAVES)",
//     "supply": 100000000,
//     "price": 2.397656,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 23977,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 32,
//     "ticker": "OMG",
//     "name": "OmiseGO",
//     "full_name": "OmiseGO (OMG)",
//     "supply": 140245398.25,
//     "price": 1.702947,
//     "vladimir_coins": 14025,
//     "vladimir_costs": 23883,
//     "coins_per_pers": 0.018236
//   },
//   {
//     "cmc_rank": 33,
//     "ticker": "QTUM",
//     "name": "Qtum",
//     "full_name": "Qtum (QTUM)",
//     "supply": 107822406,
//     "price": 2.455046,
//     "vladimir_coins": 10782,
//     "vladimir_costs": 26471,
//     "coins_per_pers": 0.01402
//   },
//   {
//     "cmc_rank": 34,
//     "ticker": "LINK",
//     "name": "Chainlink",
//     "full_name": "Chainlink (LINK)",
//     "supply": 1000000000,
//     "price": 0.670999,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 67100,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 35,
//     "ticker": "TUSD",
//     "name": "TrueUSD",
//     "full_name": "TrueUSD (TUSD)",
//     "supply": 234148207.07,
//     "price": 1.001106,
//     "vladimir_coins": 23415,
//     "vladimir_costs": 23441,
//     "coins_per_pers": 0.030446
//   },
//   {
//     "cmc_rank": 36,
//     "ticker": "NANO",
//     "name": "Nano",
//     "full_name": "Nano (NANO)",
//     "supply": 133248290,
//     "price": 1.68786,
//     "vladimir_coins": 13325,
//     "vladimir_costs": 22490,
//     "coins_per_pers": 0.017326
//   },
//   {
//     "cmc_rank": 37,
//     "ticker": "REP",
//     "name": "Augur",
//     "full_name": "Augur (REP)",
//     "supply": 11000000,
//     "price": 20.073789,
//     "vladimir_coins": 1100,
//     "vladimir_costs": 22081,
//     "coins_per_pers": 0.00143
//   },
//   {
//     "cmc_rank": 38,
//     "ticker": "LSK",
//     "name": "Lisk",
//     "full_name": "Lisk (LSK)",
//     "supply": 132000355,
//     "price": 1.750465,
//     "vladimir_coins": 13200,
//     "vladimir_costs": 23106,
//     "coins_per_pers": 0.017164
//   },
//   {
//     "cmc_rank": 39,
//     "ticker": "PAX",
//     "name": "Paxos Standard Token",
//     "full_name": "Paxos Standard Token (PAX)",
//     "supply": 193450399.76,
//     "price": 0.997508,
//     "vladimir_coins": 19345,
//     "vladimir_costs": 19297,
//     "coins_per_pers": 0.025154
//   },
//   {
//     "cmc_rank": 40,
//     "ticker": "BCN",
//     "name": "Bytecoin",
//     "full_name": "Bytecoin (BCN)",
//     "supply": 184470000000,
//     "price": 0.000944,
//     "vladimir_coins": 18447000,
//     "vladimir_costs": 17408,
//     "coins_per_pers": 23.986269
//   },
//   {
//     "cmc_rank": 41,
//     "ticker": "BCD",
//     "name": "Bitcoin Diamond",
//     "full_name": "Bitcoin Diamond (BCD)",
//     "supply": 210000000,
//     "price": 0.905133,
//     "vladimir_coins": 21000,
//     "vladimir_costs": 19008,
//     "coins_per_pers": 0.027306
//   },
//   {
//     "cmc_rank": 42,
//     "ticker": "RVN",
//     "name": "Ravencoin",
//     "full_name": "Ravencoin (RVN)",
//     "supply": 21000000000,
//     "price": 0.047609,
//     "vladimir_coins": 2100000,
//     "vladimir_costs": 99978,
//     "coins_per_pers": 2.730588
//   },
//   {
//     "cmc_rank": 43,
//     "ticker": "HOT",
//     "name": "Holo",
//     "full_name": "Holo (HOT)",
//     "supply": 177619433541.14,
//     "price": 0.001226,
//     "vladimir_coins": 17761943,
//     "vladimir_costs": 21781,
//     "coins_per_pers": 23.095503
//   },
//   {
//     "cmc_rank": 44,
//     "ticker": "ZRX",
//     "name": "0x",
//     "full_name": "0x (ZRX)",
//     "supply": 1000000000,
//     "price": 0.278501,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 27850,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 45,
//     "ticker": "ICX",
//     "name": "ICON",
//     "full_name": "ICON (ICX)",
//     "supply": 800460000,
//     "price": 0.336308,
//     "vladimir_coins": 80046,
//     "vladimir_costs": 26920,
//     "coins_per_pers": 0.104082
//   },
//   {
//     "cmc_rank": 46,
//     "ticker": "IOST",
//     "name": "IOST",
//     "full_name": "IOST (IOST)",
//     "supply": 21000000000,
//     "price": 0.013003,
//     "vladimir_coins": 2100000,
//     "vladimir_costs": 27307,
//     "coins_per_pers": 2.730588
//   },
//   {
//     "cmc_rank": 47,
//     "ticker": "BTT",
//     "name": "BitTorrent",
//     "full_name": "BitTorrent (BTT)",
//     "supply": 990000000000,
//     "price": 0.000728,
//     "vladimir_coins": 99000000,
//     "vladimir_costs": 72115,
//     "coins_per_pers": 128.727741
//   },
//   {
//     "cmc_rank": 48,
//     "ticker": "ABBC",
//     "name": "ABBC Coin",
//     "full_name": "ABBC Coin (ABBC)",
//     "supply": 1002169530.01,
//     "price": 0.297482,
//     "vladimir_coins": 100217,
//     "vladimir_costs": 29813,
//     "coins_per_pers": 0.13031
//   },
//   {
//     "cmc_rank": 49,
//     "ticker": "BTS",
//     "name": "BitShares",
//     "full_name": "BitShares (BTS)",
//     "supply": 3600570502,
//     "price": 0.054935,
//     "vladimir_coins": 360057,
//     "vladimir_costs": 19780,
//     "coins_per_pers": 0.468175
//   },
//   {
//     "cmc_rank": 50,
//     "ticker": "ZIL",
//     "name": "Zilliqa",
//     "full_name": "Zilliqa (ZIL)",
//     "supply": 12533042434.61,
//     "price": 0.016097,
//     "vladimir_coins": 1253304,
//     "vladimir_costs": 20175,
//     "coins_per_pers": 1.629647
//   },
//   {
//     "cmc_rank": 51,
//     "ticker": "NPXS",
//     "name": "Pundi X",
//     "full_name": "Pundi X (NPXS)",
//     "supply": 266962422906.54,
//     "price": 0.000653,
//     "vladimir_coins": 26696242,
//     "vladimir_costs": 17433,
//     "coins_per_pers": 34.712596
//   },
//   {
//     "cmc_rank": 52,
//     "ticker": "KMD",
//     "name": "Komodo",
//     "full_name": "Komodo (KMD)",
//     "supply": 200000000,
//     "price": 1.151707,
//     "vladimir_coins": 20000,
//     "vladimir_costs": 23034,
//     "coins_per_pers": 0.026006
//   },
//   {
//     "cmc_rank": 53,
//     "ticker": "DGB",
//     "name": "DigiByte",
//     "full_name": "DigiByte (DGB)",
//     "supply": 21000000000,
//     "price": 0.010734,
//     "vladimir_coins": 2100000,
//     "vladimir_costs": 22541,
//     "coins_per_pers": 2.730588
//   },
//   {
//     "cmc_rank": 54,
//     "ticker": "AE",
//     "name": "Aeternity",
//     "full_name": "Aeternity (AE)",
//     "supply": 309878470.5,
//     "price": 0.459119,
//     "vladimir_coins": 30988,
//     "vladimir_costs": 14227,
//     "coins_per_pers": 0.040293
//   },
//   {
//     "cmc_rank": 55,
//     "ticker": "XVG",
//     "name": "Verge",
//     "full_name": "Verge (XVG)",
//     "supply": 16555000000,
//     "price": 0.007492,
//     "vladimir_coins": 1655500,
//     "vladimir_costs": 12404,
//     "coins_per_pers": 2.152614
//   },
//   {
//     "cmc_rank": 56,
//     "ticker": "HT",
//     "name": "Huobi Token",
//     "full_name": "Huobi Token (HT)",
//     "supply": 500000000,
//     "price": 2.404252,
//     "vladimir_coins": 50000,
//     "vladimir_costs": 120213,
//     "coins_per_pers": 0.065014
//   },
//   {
//     "cmc_rank": 57,
//     "ticker": "SC",
//     "name": "Siacoin",
//     "full_name": "Siacoin (SC)",
//     "supply": 40666577747,
//     "price": 0.002862,
//     "vladimir_coins": 4066658,
//     "vladimir_costs": 11641,
//     "coins_per_pers": 5.287795
//   },
//   {
//     "cmc_rank": 58,
//     "ticker": "INB",
//     "name": "Insight Chain",
//     "full_name": "Insight Chain (INB)",
//     "supply": 10000000000,
//     "price": 0.317484,
//     "vladimir_coins": 1000000,
//     "vladimir_costs": 317484,
//     "coins_per_pers": 1.30028
//   },
//   {
//     "cmc_rank": 59,
//     "ticker": "ENJ",
//     "name": "Enjin Coin",
//     "full_name": "Enjin Coin (ENJ)",
//     "supply": 1000000000,
//     "price": 0.143229,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 14323,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 60,
//     "ticker": "BTM",
//     "name": "Bytom",
//     "full_name": "Bytom (BTM)",
//     "supply": 1407000000,
//     "price": 0.102499,
//     "vladimir_coins": 140700,
//     "vladimir_costs": 14422,
//     "coins_per_pers": 0.182949
//   },
//   {
//     "cmc_rank": 61,
//     "ticker": "STEEM",
//     "name": "Steem",
//     "full_name": "Steem (STEEM)",
//     "supply": 338319718.18,
//     "price": 0.319837,
//     "vladimir_coins": 33832,
//     "vladimir_costs": 10821,
//     "coins_per_pers": 0.043991
//   },
//   {
//     "cmc_rank": 62,
//     "ticker": "AOA",
//     "name": "Aurora",
//     "full_name": "Aurora (AOA)",
//     "supply": 10000000000,
//     "price": 0.016843,
//     "vladimir_coins": 1000000,
//     "vladimir_costs": 16843,
//     "coins_per_pers": 1.30028
//   },
//   {
//     "cmc_rank": 63,
//     "ticker": "KCS",
//     "name": "KuCoin Shares",
//     "full_name": "KuCoin Shares (KCS)",
//     "supply": 179659415,
//     "price": 1.10173,
//     "vladimir_coins": 17966,
//     "vladimir_costs": 19794,
//     "coins_per_pers": 0.023361
//   },
//   {
//     "cmc_rank": 64,
//     "ticker": "WTC",
//     "name": "Waltonchain",
//     "full_name": "Waltonchain (WTC)",
//     "supply": 100000000,
//     "price": 2.156905,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 21569,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 65,
//     "ticker": "THR",
//     "name": "ThoreCoin",
//     "full_name": "ThoreCoin (THR)",
//     "supply": 100000,
//     "price": 1036.232612,
//     "vladimir_coins": 10,
//     "vladimir_costs": 10362,
//     "coins_per_pers": 0.000013
//   },
//   {
//     "cmc_rank": 66,
//     "ticker": "QBIT",
//     "name": "Qubitica",
//     "full_name": "Qubitica (QBIT)",
//     "supply": 10000000,
//     "price": 31.358384,
//     "vladimir_coins": 1000,
//     "vladimir_costs": 31358,
//     "coins_per_pers": 0.0013
//   },
//   {
//     "cmc_rank": 67,
//     "ticker": "FCT",
//     "name": "Factom",
//     "full_name": "Factom (FCT)",
//     "supply": 9463180.54,
//     "price": 9.299112,
//     "vladimir_coins": 946,
//     "vladimir_costs": 8800,
//     "coins_per_pers": 0.00123
//   },
//   {
//     "cmc_rank": 68,
//     "ticker": "CNX",
//     "name": "Cryptonex",
//     "full_name": "Cryptonex (CNX)",
//     "supply": 210000000,
//     "price": 1.534817,
//     "vladimir_coins": 21000,
//     "vladimir_costs": 32231,
//     "coins_per_pers": 0.027306
//   },
//   {
//     "cmc_rank": 69,
//     "ticker": "DAI",
//     "name": "Dai",
//     "full_name": "Dai (DAI)",
//     "supply": 84432204.25,
//     "price": 0.988488,
//     "vladimir_coins": 8443,
//     "vladimir_costs": 8346,
//     "coins_per_pers": 0.010979
//   },
//   {
//     "cmc_rank": 70,
//     "ticker": "STRAT",
//     "name": "Stratis",
//     "full_name": "Stratis (STRAT)",
//     "supply": 99325434.17,
//     "price": 0.830795,
//     "vladimir_coins": 9933,
//     "vladimir_costs": 8252,
//     "coins_per_pers": 0.012915
//   },
//   {
//     "cmc_rank": 71,
//     "ticker": "THETA",
//     "name": "THETA",
//     "full_name": "THETA (THETA)",
//     "supply": 1000000000,
//     "price": 0.094424,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 9442,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 72,
//     "ticker": "XIN",
//     "name": "Mixin",
//     "full_name": "Mixin (XIN)",
//     "supply": 1000000,
//     "price": 180.42708,
//     "vladimir_coins": 100,
//     "vladimir_costs": 18043,
//     "coins_per_pers": 0.00013
//   },
//   {
//     "cmc_rank": 73,
//     "ticker": "ZEN",
//     "name": "Horizen",
//     "full_name": "Horizen (ZEN)",
//     "supply": 21000000,
//     "price": 12.426789,
//     "vladimir_coins": 2100,
//     "vladimir_costs": 26096,
//     "coins_per_pers": 0.002731
//   },
//   {
//     "cmc_rank": 74,
//     "ticker": "SNT",
//     "name": "Status",
//     "full_name": "Status (SNT)",
//     "supply": 6804870174,
//     "price": 0.022637,
//     "vladimir_coins": 680487,
//     "vladimir_costs": 15404,
//     "coins_per_pers": 0.884824
//   },
//   {
//     "cmc_rank": 75,
//     "ticker": "MCO",
//     "name": "Crypto.com",
//     "full_name": "Crypto.com (MCO)",
//     "supply": 31587682.36,
//     "price": 4.848609,
//     "vladimir_coins": 3159,
//     "vladimir_costs": 15316,
//     "coins_per_pers": 0.004107
//   },
//   {
//     "cmc_rank": 76,
//     "ticker": "VEST",
//     "name": "VestChain",
//     "full_name": "VestChain (VEST)",
//     "supply": 8848000000,
//     "price": 0.010759,
//     "vladimir_coins": 884800,
//     "vladimir_costs": 9520,
//     "coins_per_pers": 1.150488
//   },
//   {
//     "cmc_rank": 77,
//     "ticker": "ARDR",
//     "name": "Ardor",
//     "full_name": "Ardor (ARDR)",
//     "supply": 998999495,
//     "price": 0.074902,
//     "vladimir_coins": 99900,
//     "vladimir_costs": 7483,
//     "coins_per_pers": 0.129898
//   },
//   {
//     "cmc_rank": 78,
//     "ticker": "MAID",
//     "name": "MaidSafeCoin",
//     "full_name": "MaidSafeCoin (MAID)",
//     "supply": 452552412,
//     "price": 0.162253,
//     "vladimir_coins": 45255,
//     "vladimir_costs": 7343,
//     "coins_per_pers": 0.058844
//   },
//   {
//     "cmc_rank": 79,
//     "ticker": "DGD",
//     "name": "DigixDAO",
//     "full_name": "DigixDAO (DGD)",
//     "supply": 2000000,
//     "price": 36.197687,
//     "vladimir_coins": 200,
//     "vladimir_costs": 7240,
//     "coins_per_pers": 0.00026
//   },
//   {
//     "cmc_rank": 80,
//     "ticker": "GNT",
//     "name": "Golem",
//     "full_name": "Golem (GNT)",
//     "supply": 1000000000,
//     "price": 0.072339,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 7234,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 81,
//     "ticker": "TRUE",
//     "name": "TrueChain",
//     "full_name": "TrueChain (TRUE)",
//     "supply": 100000000,
//     "price": 0.853842,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 8538,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 82,
//     "ticker": "AION",
//     "name": "Aion",
//     "full_name": "Aion (AION)",
//     "supply": 309581662,
//     "price": 0.206196,
//     "vladimir_coins": 30958,
//     "vladimir_costs": 6383,
//     "coins_per_pers": 0.040254
//   },
//   {
//     "cmc_rank": 83,
//     "ticker": "GXC",
//     "name": "GXChain",
//     "full_name": "GXChain (GXC)",
//     "supply": 100000000,
//     "price": 1.046595,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 10466,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 84,
//     "ticker": "PAI",
//     "name": "Project Pai",
//     "full_name": "Project Pai (PAI)",
//     "supply": 1594461000,
//     "price": 0.04246,
//     "vladimir_coins": 159446,
//     "vladimir_costs": 6770,
//     "coins_per_pers": 0.207325
//   },
//   {
//     "cmc_rank": 85,
//     "ticker": "MONA",
//     "name": "MonaCoin",
//     "full_name": "MonaCoin (MONA)",
//     "supply": 65729674.87,
//     "price": 0.921117,
//     "vladimir_coins": 6573,
//     "vladimir_costs": 6054,
//     "coins_per_pers": 0.008547
//   },
//   {
//     "cmc_rank": 86,
//     "ticker": "WAX",
//     "name": "WAX",
//     "full_name": "WAX (WAX)",
//     "supply": 1850000000,
//     "price": 0.063893,
//     "vladimir_coins": 185000,
//     "vladimir_costs": 11820,
//     "coins_per_pers": 0.240552
//   },
//   {
//     "cmc_rank": 87,
//     "ticker": "MXM",
//     "name": "Maximine Coin",
//     "full_name": "Maximine Coin (MXM)",
//     "supply": 16000000000,
//     "price": 0.036334,
//     "vladimir_coins": 1600000,
//     "vladimir_costs": 58135,
//     "coins_per_pers": 2.080448
//   },
//   {
//     "cmc_rank": 88,
//     "ticker": "ELF",
//     "name": "aelf",
//     "full_name": "aelf (ELF)",
//     "supply": 1000000000,
//     "price": 0.168648,
//     "vladimir_coins": 100000,
//     "vladimir_costs": 16865,
//     "coins_per_pers": 0.130028
//   },
//   {
//     "cmc_rank": 89,
//     "ticker": "ARK",
//     "name": "Ark",
//     "full_name": "Ark (ARK)",
//     "supply": 141487250,
//     "price": 0.524313,
//     "vladimir_coins": 14149,
//     "vladimir_costs": 7418,
//     "coins_per_pers": 0.018397
//   },
//   {
//     "cmc_rank": 90,
//     "ticker": "PPT",
//     "name": "Populous",
//     "full_name": "Populous (PPT)",
//     "supply": 53252246,
//     "price": 1.067192,
//     "vladimir_coins": 5325,
//     "vladimir_costs": 5683,
//     "coins_per_pers": 0.006924
//   },
//   {
//     "cmc_rank": 91,
//     "ticker": "DENT",
//     "name": "Dent",
//     "full_name": "Dent (DENT)",
//     "supply": 100000000000,
//     "price": 0.00084,
//     "vladimir_coins": 10000000,
//     "vladimir_costs": 8403,
//     "coins_per_pers": 13.002802
//   },
//   {
//     "cmc_rank": 92,
//     "ticker": "RLC",
//     "name": "iExec RLC",
//     "full_name": "iExec RLC (RLC)",
//     "supply": 86999784.99,
//     "price": 0.702832,
//     "vladimir_coins": 8700,
//     "vladimir_costs": 6115,
//     "coins_per_pers": 0.011312
//   },
//   {
//     "cmc_rank": 93,
//     "ticker": "ABT",
//     "name": "Arcblock",
//     "full_name": "Arcblock (ABT)",
//     "supply": 186000000,
//     "price": 0.5709,
//     "vladimir_coins": 18600,
//     "vladimir_costs": 10619,
//     "coins_per_pers": 0.024185
//   },
//   {
//     "cmc_rank": 94,
//     "ticker": "SAN",
//     "name": "Santiment Network Token",
//     "full_name": "Santiment Network Token (SAN)",
//     "supply": 83337000,
//     "price": 0.86307,
//     "vladimir_coins": 8334,
//     "vladimir_costs": 7193,
//     "coins_per_pers": 0.010836
//   },
//   {
//     "cmc_rank": 95,
//     "ticker": "MANA",
//     "name": "Decentraland",
//     "full_name": "Decentraland (MANA)",
//     "supply": 2644403343.16,
//     "price": 0.051111,
//     "vladimir_coins": 264440,
//     "vladimir_costs": 13516,
//     "coins_per_pers": 0.343847
//   },
//   {
//     "cmc_rank": 96,
//     "ticker": "ETP",
//     "name": "Metaverse ETP",
//     "full_name": "Metaverse ETP (ETP)",
//     "supply": 100000000,
//     "price": 0.74916,
//     "vladimir_coins": 10000,
//     "vladimir_costs": 7492,
//     "coins_per_pers": 0.013003
//   },
//   {
//     "cmc_rank": 97,
//     "ticker": "XZC",
//     "name": "Zcoin",
//     "full_name": "Zcoin (XZC)",
//     "supply": 21400000,
//     "price": 6.927669,
//     "vladimir_coins": 2140,
//     "vladimir_costs": 14825,
//     "coins_per_pers": 0.002783
//   },
//   {
//     "cmc_rank": 98,
//     "ticker": "JCT",
//     "name": "Japan Content Token",
//     "full_name": "Japan Content Token (JCT)",
//     "supply": 2500000000,
//     "price": 0.173517,
//     "vladimir_coins": 250000,
//     "vladimir_costs": 43379,
//     "coins_per_pers": 0.32507
//   },
//   {
//     "cmc_rank": 99,
//     "ticker": "ELA",
//     "name": "Elastos",
//     "full_name": "Elastos (ELA)",
//     "supply": 34441382.03,
//     "price": 3.273497,
//     "vladimir_coins": 3444,
//     "vladimir_costs": 11274,
//     "coins_per_pers": 0.004478
//   },
//   {
//     "cmc_rank": 100,
//     "ticker": "R",
//     "name": "Revain",
//     "full_name": "Revain (R)",
//     "supply": 484450000,
//     "price": 0.102341,
//     "vladimir_coins": 48445,
//     "vladimir_costs": 4958,
//     "coins_per_pers": 0.062992
//   }
// ];

// PURE FUNCTIONS
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min; 
}

// SYNC FUNCTIONS
function render() {
  var back = [
    'AliceBlue',
    'AntiqueWhite',
    'Aqua',
    'Aquamarine',
    'Azure',
    'Beige',
    'Bisque',
    'BlanchedAlmond',
    'Blue',
    'BlueViolet',
    'Brown',
    'BurlyWood',
    'CadetBlue',
    'Chartreuse',
    'Chocolate',
    'Coral',
    'CornflowerBlue',
    'Cornsilk',
    'Crimson',
    'Cyan',
    'DarkBlue',
    'DarkCyan',
    'DarkGoldenRod',
    'DarkGray',
    'DarkGrey',
    'DarkGreen',
    'DarkKhaki',
    'DarkMagenta',
    'DarkOliveGreen',
    'Darkorange',
    'DarkOrchid',
    'DarkRed',
    'DarkSalmon',
    'DarkSeaGreen',
    'DarkSlateBlue',
    'DarkSlateGray',
    'DarkSlateGrey',
    'DarkTurquoise',
    'DarkViolet',
    'DeepPink',
    'DeepSkyBlue',
    'DimGray',
    'DimGrey',
    'DodgerBlue',
    'FireBrick',
    'FloralWhite',
    'ForestGreen',
    'Fuchsia',
    'Gainsboro',
    'GhostWhite',
    'Gold',
    'GoldenRod',
    'Gray',
    'Grey',
    'Green',
    'GreenYellow',
    'HoneyDew',
    'HotPink',
    'IndianRed',
    'Indigo',
    'Ivory',
    'Khaki',
    'Lavender',
    'LavenderBlush',
    'LawnGreen',
    'LemonChiffon',
    'LightBlue',
    'LightCoral',
    'LightCyan',
    'LightGoldenRodYellow',
    'LightGray',
    'LightGrey',
    'LightGreen',
    'LightPink',
    'LightSalmon',
    'LightSeaGreen',
    'LightSkyBlue',
    'LightSlateGray',
    'LightSlateGrey',
    'LightSteelBlue',
    'LightYellow',
    'Lime',
    'LimeGreen',
    'Linen',
    'Magenta',
    'Maroon',
    'MediumAquaMarine',
    'MediumBlue',
    'MediumOrchid',
    'MediumPurple',
    'MediumSeaGreen',
    'MediumSlateBlue',
    'MediumSpringGreen',
    'MediumTurquoise',
    'MediumVioletRed',
    'MidnightBlue',
    'MintCream',
    'MistyRose',
    'Moccasin',
    'NavajoWhite',
    'Navy',
    'OldLace',
    'Olive',
    'OliveDrab',
    'Orange',
    'OrangeRed',
    'Orchid',
    'PaleGoldenRod',
    'PaleGreen',
    'PaleTurquoise',
    'PaleVioletRed',
    'PapayaWhip',
    'PeachPuff',
    'Peru',
    'Pink',
    'Plum',
    'PowderBlue',
    'Purple',
    'Red',
    'RosyBrown',
    'RoyalBlue',
    'SaddleBrown',
    'Salmon',
    'SandyBrown',
    'SeaGreen',
    'SeaShell',
    'Sienna',
    'Silver',
    'SkyBlue',
    'SlateBlue',
    'SlateGray',
    'SlateGrey',
    'Snow',
    'SpringGreen',
    'SteelBlue',
    'Tan',
    'Teal',
    'Thistle',
    'Tomato',
    'Turquoise',
    'Violet',
    'Wheat',
    'White',
    'WhiteSmoke',
    'Yellow',
    'YellowGreen'
    ]
    var colo = []

    for (let i = 0; i < n_data_voucer.length; i++) {
        var rand = back[Math.floor(Math.random() * back.length)];
        colo.push(rand);
    }
    
    colo = ['#2175cb', '#6ac800', '#ff8201', '#ffca00', '#ff3768'] 
    
    if(n_data_voucer.length/2 != colo.length ){
        colo.push('#4939c1')
    }
    const padding   = { top: 20, right: 20, bottom: 20, left: 20};
    const width     = 500 - padding.left - padding.right;
    const height    = 500 - padding.top - padding.bottom;
    const radius    = Math.min(width, height) / 2;
    const spins     = 5;
    const degrees   = spins * 360;
    const color     = d3.scaleOrdinal(colo);
    let counter     = 0;
    let picked      = 1000;

    let fontSize;
    if(selection > 50) {
        fontSize = '10px';
    } else {
        fontSize = '18px';
    }

    let svg = d3.select('#chart').selectAll('svg').data([null]);
    svg = svg
        .enter().append('svg')
        .merge(svg)
        .data([data])
            .attr('width', 500)
            .attr('height', 500);
    
    const container = svg.append('g')
        .attr('class', 'chartcontainer')
        .attr('transform', `translate(${width/2 + padding.left},${height/2 + padding.top})`);
    
    const wheel = container.append('g')
        .attr('class', 'wheel');
    
    const pie = d3.pie().sort(null).value(function(d){return 1;});
    
    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);
    
    const arcs = wheel.selectAll('g.slice')
        .data(pie)
        .enter()
        .append('g')
            .attr('class', 'slice');
    
    arcs.append('path')
        .attr('fill', function(d,i){return color(i);})
        .attr('d', function(d){return arc(d);});
    
    arcs.append("text").attr("transform", function(d){
        d.innerRadius = 0;
        d.outerRadius = radius;
        d.angle = (d.startAngle + d.endAngle)/2;
        return `rotate(${(d.angle * 180 / Math.PI - 90)})translate(${d.outerRadius -10})`;
        })
            .attr("text-anchor", "end")
        .text( function(d, i) {
            return data[i].ticker;
        })
        .style('font-size', fontSize);
    
    // arrow
    svg.append('g')
            .attr('class', 'arrow')
            .attr('transform', `translate(${(width + padding.left + padding.right)/2 - 15}, 12)`)
        .append('path')
            .attr('d', `M0 0 H30 L 15 ${Math.sqrt(3)/2*30}Z`)
            .style('fill', '#000809');
    
    // push button
    const push = d3.select('#push');
    let result = d3.select('#result').data([null]);
                result = result
                    .enter()
                    .append('text')
                        .attr('class', 'result')
                    .merge(result)
                        .html('<img src="/assets/icons/27.png" width="80%">')
                        .style('font-size', '30px')
                        .style('font-weight', '700');
    

    push.on('click', spin);
    
    // FUNCTIONS
    function spin(d){
        $('#totok').val(parseInt($('#totok').val())-1)
        $('#isbuttontukar').prop('disabled', true)
        $('#push').prop('disabled', true)
        counter++;
    
        const piedegree         = 360 / data.length;
        const randomAssetIndex  = getRandomInt(0, data.length);
        const randomPieMovement = getRandomInt(1, piedegree);
        
        rotation = (data.length - randomAssetIndex) * piedegree - randomPieMovement + degrees;
    
        wheel.transition()
            .duration(3000)
            .attrTween('transform', rotTween)
            .ease(d3.easeCircleOut)
            .on('end', function(){
    
                // let result = d3.select('#result').data([null]);
                // result = result
                //     .enter()
                //     .append('text')
                //         .attr('class', 'result')
                //     .merge(result)
                //         .text(data[randomAssetIndex].ticker)
                //         .style('font-size', '30px')
                //         .style('font-weight', '700');
                
                // let rank = d3.select('.spin-result-rank').data([null]);
                // rank = rank
                // .enter()
                // .append('text')
                //     .attr('class', '')
                // .merge(rank)
                //     .text(` ${top100[randomAssetIndex].cmc_rank}`);

                // let price = d3.select('.spin-result-price').data([null]);
                // price = price
                // .enter()
                // .append('text')
                //     .attr('class', '')
                // .merge(price)
                //     .text(` $${top100[randomAssetIndex].price}`);

                // let vladimir = d3.select('.spin-result-vladimir').data([null]);
                // vladimir = vladimir
                // .enter()
                // .append('text')
                //     .attr('class', '')
                // .merge(vladimir)
                //     .text(` $${top100[randomAssetIndex].vladimir_costs}`);

                // let coins = d3.select('.spin-result-coins').data([null]);
                // coins = coins
                // .enter()
                // .append('text')
                //     .attr('class', '')
                // .merge(coins)
                //     .text(` ${top100[randomAssetIndex].coins_per_pers}`);

                
                        var hasil = ''
                        let isloop = $('#total-token').val()
                        if( isloop > 1){

                            let loop_kd_voucher = []
                            let loop_token = []
                            let loop_nm_voucher = []
                            isloop = isloop-1;
                            loop_kd_voucher.push({
                                'kd' : top100[randomAssetIndex].code,
                                'spin' : 1
                            })
                            loop_nm_voucher.push(top100[randomAssetIndex].name)
                            
                            
                            for (let i = 0; i < isloop; i++) {
                                let rand = Math.floor(Math.random()*top100.length)
                                loop_kd_voucher.push({
                                    'kd' : top100[rand].code,
                                    'spin' : 0
                                })
                                loop_nm_voucher.push(top100[rand].name)
                            }

                            for (let i = 0; i < isloop+1; i++) {
                                loop_token.push(data_token[i])
                            }
                            claimtokloop(loop_kd_voucher, loop_token, d3)
                            
                        }else{
                            
                            hasil = top100[randomAssetIndex].name
                            claimtok(top100[randomAssetIndex].code, data_token[Math.floor(Math.random()*data_token.length)], hasil, d3)
                        }

            });
    }
    
    function rotTween() {
        let i = d3.interpolate(0, rotation);
        return function(t) {
            return `rotate(${i(t)})`;
        };
    }
}

function getData(value) {
    let array = [];

    for(let i = 0; i < value; i++) {
        array.push(rawData[i]);
    }

    return array;
}

function updateSelection(e) {
    buttons.forEach(button => {
        button.classList.remove('current');
    });

    if(e.target.classList.contains('difficulty__button')) {
        e.target.classList.add('current');
    }

    selection = document.querySelector('.current').value;
    data = getData(selection);
    render();
}

function closeModal() {
    modal.style.display = 'none';
    window.location.reload()
}

function outsideClick(e) {
    if(e.target == modal) {
        modal.style.display = 'none';
        window.location.reload()
    }
}

// EVENT LISTENERS
box.addEventListener('click', updateSelection);
closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', outsideClick);
window.onload = render;

function tukarkan() {
   $('#push').trigger('click');
}

$('.closeBtn').on('click', function () {
    // if(!$('#modal').is(':visible')){
        
    // }
})


function claimtok(code, token, hasil, d3) {
    $.ajax({
        datatype: 'json',
        type: 'post',
        url : 'claimtoken',
        data : {
            'code' : code,
            'token' : token
        },
        success: function(result){
            result = JSON.parse(result, true)
            let code = result.code
            let data = result.data
            if(code == 0){
                if($('#totok').val() == 0){
                    $('#maindong').hide()
                }
                
                let name = d3.select('.spin-result-name').data([null]);
                name = name
                .enter()
                .append('text')
                .attr('class', '')
                .merge(name)
                .html(`${data.nm_voucher}`)
                
                let details = d3.select('#modal').data([null]);
                    details = details
                        .enter()
                        .merge(details)
                            .style('display', 'block');

                var tada = $("#tada")[0];
                tada.play();

                callemail(data)
            }else{
                $('#modal-error').css('display', 'block')
            }
        }
    })
}

function claimtokloop(code, token, d3) {

    $.ajax({
        datatype: 'json',
        type: 'post',
        url : 'claimtokenloop',
        data : {
            'code' : code,
            'token' : token
        },
        success: function(result){
            result = JSON.parse(result, true)
            let code = result.code
            let data = result.data

            if(code == 0){
                let nom = 1
                let has = ''
                let hasil = ''
                const counts = {};
                const sampleArray = data.nm_voucher;
                sampleArray.forEach(function (x) { counts[x] = (counts[x] || 0) + 1; });
                
                let tot = 0;
                for(let key in counts) {
                    ++tot;
                }
                let colsm = tot == 1 ? 12 : 6
                let lastElement;
                if(tot % 2 != 0){
                    for (lastElement in counts);
                    lastElement;
                }

                let row = '<div class="row">'
                Object.entries(counts).forEach(entry => {
                    const [key, value] = entry;
                    if(key == lastElement){
                        colsm = 12
                    }
                    row += `<div class="col-lg-${colsm}">`
                    row += '<span style="font-size: 19px;">•' + (value!=1 ? ' x'+value+' ' : '') + key + '</span>'
                    row += '</div>'
                });

                row += '</div>'
                
                hasil = row

                if($('#totok').val() == 0){
                    $('#maindong').hide()
                }
                
                let name = d3.select('.spin-result-name').data([null]);
                name = name
                .enter()
                .append('text')
                .attr('class', '')
                .merge(name)
                .html(`${hasil}`)
                
                let details = d3.select('#modal').data([null]);
                    details = details
                        .enter()
                        .merge(details)
                            .style('display', 'block');
                    
                var tada = $("#tada")[0];
                tada.play();

                callemailloop(data)
            }else{
                $('#modal-error').css('display', 'block')
            }
        }
    })
}

function callemail(params) {
    
    $.ajax({
        datatype: 'json',
        type: 'post',
        url : 'sendredeemtoken',
        data : {
            'id_user' : params.iduser,
            'nm_dealer' : params.nm_dealer,
            'nm_voucher' : params.nm_voucher,
            'email' : params.email
        },
        success: function(result){

        }
    })
}

function callemailloop(params) {
    
    $.ajax({
        datatype: 'json',
        type: 'post',
        url : 'sendredeemtokenloop',
        data : params,
        success: function(result){

        }
    })
}

function kembalilah(url) {
    window.location.href = url
}