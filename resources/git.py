from github import Github
import argparse
import os
import sys

class GithubApi():
    def __init__(self,token):
        self.token = token
        self.github = Github(login_or_token=token)

    def createRepo(self,org,repo,repoReadmeContents,repo_privacy):
        try:
            print(org,repo,repoReadmeContents,repo_privacy)
            orgObject = self.github.get_organization(org)
            repoObject = orgObject.create_repo(repo, description = "Repo created from python", private = repo_privacy)
            repoObject.create_file("README.md", "Initial Commit", repoReadmeContents)
            print("Repo Created")
            return {"status": "OK", "message": "Repo ${repo} Created"}
        except Exception as e:
            print(e)
            return {"status": "NOTOK", "message": str(e)}

def main():

    if "GIT_TOKEN" in os.environ:
        git = GithubApi(os.environ["GIT_TOKEN"])
    else:
        sys.exit("No GIT_TOKEN found in env variables")

    parser = argparse.ArgumentParser(prog='git.py', description='Git API Script')
    parser.add_argument('-a', '--action', choices=['createRepo'], required=True, help='Set the action for the script')
    args = parser.parse_args()

    if(args.action or args.a):
        if(args.action == "createRepo"):
            if("GIT_ORGANIZATION" in os.environ):
                GIT_ORGANIZATION = os.environ["GIT_ORGANIZATION"]
            else:
                sys.exit("No GIT_ORGANIZATION env variable set, exiting...")

            if("GIT_REPO_NAME" in os.environ):
                GIT_REPO_NAME = os.environ["GIT_REPO_NAME"]
            else:
                sys.exit("No GIT_REPO_NAME env variable set, exiting...")
            
            if("GIT_REPO_PRIVACY_SETTING" in os.environ):
                if(os.environ["GIT_REPO_PRIVACY_SETTING"] == "Y" or os.environ["GIT_REPO_PRIVACY_SETTING"].upper() == "YES"):
                    GIT_REPO_PRIVACY_SETTING = True
                else:
                    GIT_REPO_PRIVACY_SETTING = False
            else:
                GIT_REPO_PRIVACY_SETTING = False

            if("GIT_README_CONTENT" in os.environ):
                GIT_README_CONTENT = os.environ["GIT_README_CONTENT"]
            else:
                GIT_README_CONTENT = ""

            git.createRepo(GIT_ORGANIZATION, GIT_REPO_NAME, GIT_README_CONTENT, GIT_REPO_PRIVACY_SETTING)
        
    else:
        print("Action is missing")

if __name__ == "__main__":
    main()


# Use below command to run the script
# python3 -m pip install PyGithub
# git.py -a createRepo

# Useful links
# https://github.com/PyGithub/PyGithub
# https://pygithub.readthedocs.io/en/latest/examples/MainClass.html