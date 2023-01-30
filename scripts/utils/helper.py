from ape import chain
import subprocess

w3 = chain.provider.web3
balance_call = "balanceOf(address)(uint256)"
transfer_call = "transfer(address,uint256)(bool)"


def set_balance(account, amount):
    chain.set_balance(account, amount)


def get_block():
    return chain.blocks[-1].number


def impersonate(account):
    subprocess.run(
        ["cast", "rpc", "anvil_impersonateAccount", f"{account}"],
        capture_output=True,
    )


def balance_of(token, owner):
    return int(
        subprocess.run(
            ["cast", "call", f"{token}", f"{balance_call}", f"{owner}"],
            capture_output=True,
            text=True,
        ).stdout[:-1]
    )


def transfer_from(token, sender, to, amount):
    subprocess.run(
        [
            "cast",
            "send",
            f"{token}",
            "--from",
            f"{sender}",
            f"{transfer_call}",
            f"{to}",
            f"{amount}",
        ],
        capture_output=True,
    )
