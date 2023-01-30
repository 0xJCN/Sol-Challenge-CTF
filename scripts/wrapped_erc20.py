from ape import accounts, project
from .utils.helper import w3


ETH_AMOUNT = w3.to_wei(10, "ether")


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.WrappedERC20Challenge.deploy(
        sender=deployer,
        value=ETH_AMOUNT,
    )

    weth = challenge.WETH()
    wtoken = challenge.wwETH()

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.WrappedERC20Attacker.deploy(
        challenge.address,
        weth,
        wtoken,
        sender=attacker,
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
