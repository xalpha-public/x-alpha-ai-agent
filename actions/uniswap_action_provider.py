from typing import Any
from coinbase_agentkit.action_providers import ActionProvider, create_action
from coinbase_agentkit.wallet_providers import EvmWalletProvider, EthAccountWalletProvider
from coinbase_agentkit.network import Network
from .uniswap_router import Uniswap
from coinbase_agentkit.action_providers.wow.schemas import WowBuyTokenSchema, WowSellTokenSchema

SUPPORTED_CHAINS = ["8453", "84532"]

class UniswapActionProvider(ActionProvider[EthAccountWalletProvider]):
    """Provides actions for interacting with Uniswap protocol."""

    def __init__(self):
        """Initialize Uniswap action provider."""
        super().__init__("uniswap", [])
        self.weth_address = "0x4200000000000000000000000000000000000006"
        self.native_token_address = "0x0000000000000000000000000000000000000000"
        
    @create_action(
        name="buy_token",
        description="""
        This tool can only be used to buy a UNISWAP v3/v4 token with ETH.
        Do not use this tool for any other purpose, or trading other assets.

        Inputs:
        - Token contract address
        - Amount of ETH to spend (in wei)

        Important notes:
        - The amount is a string and cannot have any decimal points, since the unit of measurement is wei.
        - Make sure to use the exact amount provided, and if there's any doubt, check by getting more information before continuing with the action.
        - 1 wei = 0.000000000000000001 ETH
        - Minimum purchase amount is 100000000000000 wei (0.0000001 ETH)""",
        schema=WowBuyTokenSchema,
    )
    def buy_token(self, wallet_provider: EthAccountWalletProvider, args: dict[str, Any]) -> str:
        """Buy WOW tokens with ETH.

        Args:
            wallet_provider (EthAccountWalletProvider): The wallet provider to buy tokens from.
            args (dict[str, Any]): Input arguments containing contract_address and amount_eth_in_wei.

        Returns:
            str: A message containing the purchase details or error message.

        """
        try:
            
            account = wallet_provider.config.account
            uniswap = Uniswap(
                wallet_address=account.address,
                private_key=account._private_key,
                provider=wallet_provider.config.rpc_url,  # Used to auto-detect chain
                web3=wallet_provider.web3
            )
            tx_hash = uniswap.make_trade(
                from_token=self.weth_address,
                to_token=args["contract_address"],
                amount=int(args["amount_eth_in_wei"]),
                fee=3000,         # e.g., 3000 for a 0.3% Uniswap V3 pool
                slippage=0.5,     # non-functional right now. 0.5% slippage tolerance
                pool_version="v3"  # can be "v3" or "v4"
            )
            # print(f"Swap transaction sent! Tx hash: {tx_hash.hex()}")
            return f"Purchased Uniswap ERC20 token with transaction hash: {tx_hash.hex()}"
        except Exception as e:
            return f"Error buying Uniswap ERC20 token: {e!s}"

    @create_action(
        name="sell_token",
        description="""
        This tool can only be used to sell a Zora Wow ERC20 memecoin (also can be referred to as a bonding curve token) for ETH.
        Do not use this tool for any other purpose, or trading other assets.

        Inputs:
        - WOW token contract address
        - Amount of tokens to sell (in wei)

        Important notes:
        - The amount is a string and cannot have any decimal points, since the unit of measurement is wei.
        - Make sure to use the exact amount provided, and if there's any doubt, check by getting more information before continuing with the action.
        - 1 wei = 0.000000000000000001 ETH
        - Minimum purchase amount to account for slippage is 100000000000000 wei (0.0000001 ETH)""",
        schema=WowSellTokenSchema,
    )
    def sell_token(self, wallet_provider: EthAccountWalletProvider, args: dict[str, Any]) -> str:
        """Sell WOW tokens for ETH.

        Args:
            wallet_provider (EthAccountWalletProvider): The wallet provider to sell tokens from.
            args (dict[str, Any]): Input arguments containing contract_address and amount_tokens_in_wei.

        Returns:
            str: A message containing the sell details or error message.

        """
        try:
            account = wallet_provider.config.account
            uniswap = Uniswap(
                wallet_address=account.address,
                private_key=account._private_key,
                provider=wallet_provider.config.rpc_url,  # Used to auto-detect chain
                web3=wallet_provider.web3
            )
            tx_hash = uniswap.make_trade(
                from_token=args["contract_address"],
                to_token=self.weth_address,
                amount=args["amount_tokens_in_wei"],
                fee=3000,         # e.g., 3000 for a 0.3% Uniswap V3 pool
                slippage=0.5,     # non-functional right now. 0.5% slippage tolerance
                pool_version="v3"  # can be "v3" or "v4"
            )
            print(f"Swap transaction sent! Tx hash: {tx_hash.hex()}")
            return f"Sold Uniswap ERC20 token with transaction hash: {tx_hash}"
        except Exception as e:
            return f"Error selling Uniswap ERC20 token: {e!s}"

    def supports_network(self, network: Network) -> bool:
        """Check if network is supported by WOW protocol.

        Args:
            network (Network): The network to check support for.

        Returns:
            bool: True if network is supported, False otherwise.

        """
        return network.protocol_family == "evm" and network.chain_id in SUPPORTED_CHAINS


def uniswap_action_provider() -> UniswapActionProvider:
    """Create a new UniswapActionProvider instance."""
    return UniswapActionProvider()



