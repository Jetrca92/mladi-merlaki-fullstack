/**
 * @vitest-environment happy-dom
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StockInfo from './StockInfo.vue'

describe('StockInfo Tests!', () => {
    const stock = {
        name: 'Apple',
        symbol: 'APPL',
        price: 500,
        country: 'US',
        sector: 'Technology',
        market_cap: 1000000000000,
        volume: 50000000000,
        dividend: 0,
    }

    it('renders stock name and symbol correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('h3.title.is-3').text()).toBe('Apple (APPL)')
    })

    it('renders stock price correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('h1.title.is-1.mb-3').text()).toBe('$500')
    })

    it('renders country correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('div.content p:nth-child(1)').text()).toBe('Country: US')
    })

    it('renders sector correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('div.content p:nth-child(2)').text()).toBe('Sector: Technology')
    })

    it('renders market cap correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('div.content p:nth-child(3)').text()).toBe('Market Cap: $1.000.000.000.000')
    })

    it('renders 24h trading volume correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('div.content p:nth-child(4)').text()).toBe('24 Hour Trading Volume: $50.000.000.000')
    })

    it('renders dividend correctly', () => {
        const wrapper = mount(StockInfo, {
            props: {
                stock
            }
        })
        expect(wrapper.find('div.content p:nth-child(5)').text()).toBe('Dividend: $0')
    })
})
