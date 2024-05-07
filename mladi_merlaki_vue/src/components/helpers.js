export const sharesInPortfolio = (coin, store) => {
    const portfolio = store.state.portfolio;
    const cryptoPortfolio = portfolio.crypto.find(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    return cryptoPortfolio ? cryptoPortfolio.shares : 0
}


export const valueOfShares = (coin, store) => {
    const portfolio = store.state.portfolio;
    const cryptoPortfolio = portfolio.crypto.find(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    return cryptoPortfolio ? cryptoPortfolio.shares * cryptoPortfolio.coin.price : 0
}


export const averageBuyPrice = (coin, store) => {
    const transactions = store.state.portfolio.transactions
    if (!transactions || transactions.length === 0) {
        return null; // Return null if transactions is null or empty
    }
    const symbolTransactions = transactions.filter(transaction => transaction.symbol === coin.symbol && transaction.type === "buy")
    if (symbolTransactions.length === 0) {
        return null; // Return null if there are no transactions for the symbol
    }
    const totalAmount = symbolTransactions.reduce((acc, transaction) => acc + (transaction.shares * transaction.price), 0)
    const totalShares = symbolTransactions.reduce((acc, transaction) => acc + transaction.shares, 0)
    return totalAmount / totalShares
}
