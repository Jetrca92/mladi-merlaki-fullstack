import { sharesInPortfolio, valueOfShares, averagePrice } from "./helpers"
import { describe, it, expect } from 'vitest'

const mockStore = {
    state: {
        portfolio: {
            crypto: [
                { coin: { 
                    name: 'Bitcoin',
                    symbol: 'BTC',
                    logo: 'path/to/bitcoin/logo.svg',
                    price: 50000,
                    market_cap: 1000000000000,
                    volume: 50000000000 }, shares: 10 },    
            ],
            transactions : [
                {
                    "owner": 1,
                    "symbol": "BTC",
                    "asset_class": "crypto",
                    "shares": 6,
                    "price": 60000,
                    "type": "buy",
                    "date": "2024-05-08T12:00:00Z"
                },
                {
                    "owner": 1,
                    "symbol": "BTC",
                    "asset_class": "crypto",
                    "shares": 4,
                    "price": 50000,
                    "type": "buy",
                    "date": "2024-05-08T12:00:00Z"
                },
                {
                    "owner": 1,
                    "symbol": "BTC",
                    "asset_class": "crypto",
                    "shares": 4,
                    "price": 50000,
                    "type": "sell",
                    "date": "2024-05-08T12:00:00Z"
                },
                {
                    "owner": 1,
                    "symbol": "DOGE",
                    "asset_class": "crypto",
                    "shares": 400,
                    "price": 0.6,
                    "type": "sell",
                    "date": "2024-05-08T12:00:00Z"
                },
            ]
        }
    }
}


describe('sharesInPortfolio function', () => {
    it('returns the correct number of shares for a given coin', () => {
        const coin = { symbol: 'BTC' }
        expect(sharesInPortfolio(coin, mockStore)).toBe(10)
    })
  
    it('returns 0 shares for a coin not in the portfolio', () => {
        const coin = { symbol: 'LTC' }
        expect(sharesInPortfolio(coin, mockStore)).toBe(0)
    })

    it('handles a coin object with missing symbol property', () => {
        expect(sharesInPortfolio({}, mockStore)).toBe(0)
    })
})


describe('valueOfShares function', () => {
    it('returns the correct value of shares for a given coin', () => {
        const coin = { symbol: 'BTC' }
        expect(valueOfShares(coin, mockStore)).toBe(500000)
    })

    it('returns 0 value for a coin not in the portfolio', () => {
        const coin = { symbol: 'LTC' }
        expect(valueOfShares(coin, mockStore)).toBe(0)
    })

    it('handles a coin object with missing symbol property'), () => {
        expect(valueOfShares({}, mockStore)).toBe(0)
    }
}) 


describe('averagePrice function', () => {
    it('returns the correct average buy price for a given coin'), () => {
        const coin = { symbol: 'BTC'}
        // (6 * 60000 + 4* 50000) / 10 = 56000
        expect(averagePrice(coin, mockStore)).toBe(56000)
    }

    it('returns null if no transactions matching the symbol'), () => {
        const coin = { symbol: 'ETH'}
        expect(averagePrice(coin, mockStore)).toBeNull
    }

    it('returns null when only sell transactions matching the symbol'), () => {
        const coin = { symbol: 'DOGE'}
        expect(averagePrice(coin, mockStore)).toBeNull
    }
})
