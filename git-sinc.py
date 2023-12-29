import git
import sys
import os


def filter_branches(branches, current_branch):
    ignore = ["HEAD", "feature", "fix", "feat"]
    new_list = []

    for branch in branches:
        branch = str(branch)
        if any(map(branch.__contains__, ignore)) == False:
            branch = branch.replace("origin/", "")
            if branch != str(current_branch):
                new_list.append(branch)

    return new_list


if __name__ == "__main__":
    repo = git.Repo(".")
    repo.git.pull()
    remote_refs = repo.remote().refs
    current_branch = repo.active_branch

    file_to_sync = (
        input("Digite o nome do arquivo que deseja sincronizar: ")
        if sys.argv[1] == None
        else sys.argv[1]
    )
    if not os.path.exists(file_to_sync):
        print("Arquivo não encontrado")
        sys.exit(1)

    confirmation = input(
        f"Você tem certeza que deseja sincronizar o arquivo {file_to_sync} da branch {current_branch} com todas as branches? (y/n) "
    )

    branches_that_will_sync = filter_branches(remote_refs, current_branch)

    confirmation2 = input(
        f"O sync vai acontecer para as branches: {branches_that_will_sync}. Deseja continuar? (y/n) "
    )

    if confirmation == "y" and confirmation2 == "y":
        for ref in branches_that_will_sync:
            try:
                if ref != "HEAD" and str(ref) != str(current_branch):
                    print(f"Sincronizando com a branch {ref}")
                    repo.git.checkout(ref)
                    repo.git.pull()
                    repo.git.checkout(current_branch, file_to_sync)
                    repo.git.add(file_to_sync)
                    repo.git.commit(
                        "-m", f"Synced {file_to_sync} from {current_branch}"
                    )
                    repo.git.push()
            except Exception as e:
                print(e)
                continue

        repo.git.checkout(current_branch)
