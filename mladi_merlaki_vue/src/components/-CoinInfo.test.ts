/**
 * @vitest-environment happy-dom
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import CoinInfo from './CoinInfo.vue'

describe('CoinInfo Tests!', () => {
    const coin = {
        name: 'Bitcoin',
        symbol: 'BTC',
        logo: 'path/to/bitcoin/logo.svg',
        price: 50000,
        market_cap: 1000000000000,
        volume: 50000000000
    }

    it('renders coin name and symbol correctly', () => {
        const wrapper = mount(CoinInfo, {
            props: {
                coin
            }
        })
        expect(wrapper.find('h3.title.is-3').text()).toBe('Bitcoin (BTC)')
    })

    it('renders coin price correctly', () => {
        const wrapper = mount(CoinInfo, {
            props: {
                coin
            }
        })
        expect(wrapper.find('h1.title.is-1.mb-3').text()).toBe('$50.000')
    })

    it('renders market cap correctly', () => {
        const wrapper = mount(CoinInfo, {
            props: {
                coin
            }
        })
        expect(wrapper.find('div.content p:nth-child(1)').text()).toBe('Market Cap: $1.000.000.000.000')
    })

    it('renders 24-hour trading volume correctly', () => {
        const wrapper = mount(CoinInfo, {
            props: {
                coin
            }
        })
        expect(wrapper.find('div.content p:nth-child(2)').text()).toBe('24 Hour Trading Volume: $50.000.000.000')
    })
})
