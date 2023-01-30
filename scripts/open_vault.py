from ape import accounts, project
from .utils.helper import w3


ETH_IN_VAULT = w3.to_wei(1, "ether")


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.OpenVaultChallenge.deploy(sender=deployer, value=ETH_IN_VAULT)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    project.OpenVaultAttacker.deploy(challenge.address, sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
