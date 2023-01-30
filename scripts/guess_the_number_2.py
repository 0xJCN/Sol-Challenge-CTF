from ape import accounts, project


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.GuessTheNumberChallenge2.deploy(sender=deployer)

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit

    # addmod(a, a++, 10)
    # a = 3, a++ = 4
    # 3 + 4 = 7, 7 % 10 = 7
    challenge.guess(3, sender=attacker)

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
