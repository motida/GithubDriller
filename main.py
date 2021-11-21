import json
import pytz
from datetime import datetime

from pydriller import RepositoryMining, Commit, Modification, ModificationType

GITHUB_REPO = '~/kernel/linux'
OUTPUT_FILE = 'kernel_github_2020.jl'
YEAR = 2020


def main(year):
    f = open(OUTPUT_FILE, 'w')
    # Between 2 dates
    dt1 = datetime(year, 1, 1, 0, 0, 0)
    dt2 = datetime(year, 12, 31, 23, 59, 59, 999)
    commits = RepositoryMining(GITHUB_REPO, since=dt1, to=dt2).traverse_commits()

    counter = 0
    for commit in commits:
        commit_doc = {'commit': commit.hash,
                      'author': {'name': commit.author.name,
                                 'email': commit.author.email,
                                 'date': commit.author_date.astimezone(pytz.utc).strftime(
                                     "%Y-%m-%d %H:%M:%S UTC"),
                                 'tz_offset': commit.author_date.strftime("%z")},
                      'committer': {'name': commit.committer.name,
                                    'email': commit.committer.email,
                                    'date': commit.committer_date.astimezone(pytz.utc).strftime(
                                        "%Y-%m-%d %H:%M:%S UTC"),
                                    'tz_offset': commit.committer_date.strftime("%z")},
                      'message': commit.msg}

        modifications_doc = []
        for modification in commit.modifications:
            modification_doc = {'filename': modification.filename,
                                'old_path': modification.old_path,
                                'new_path': modification.new_path,
                                'added': modification.added,
                                'removed': modification.removed,
                                'nloc': modification.nloc,
                                'source_len_before': len(modification.source_code_before) if
                                modification.source_code_before else None,
                                'source_len': len(modification.source_code) if
                                modification.source_code else None}
            modifications_doc.append(modification_doc)
        commit_doc['modifications'] = modifications_doc
        json.dump(commit_doc, f)
        f.write('\n')
        counter += 1
        if counter % 1000 == 0:
            print(counter)
    f.close()
    print(counter)


if __name__ == '__main__':
    main(YEAR)

