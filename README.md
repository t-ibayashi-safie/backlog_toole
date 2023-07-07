## Summary

BacklogでIssueにマイルストーンを一括付与するスクリプトです。


## Detail
Backlogの一括更新機能でマイルストーンを更新すると、既存のマイルストーンが解除されてしまいます。
このスクリプトでは、既存のマイルストーンを解除することなく、マイルストーンを一括付与することができます。


## How to run

**.envファイルを作成**

**付与したいマイルストーンをBacklog上で作成**

**必要な情報を取得**
```bash
python -m backlog_tools.fetch_milestones > ./data/milestones.json
python -m backlog_tools.fetch_statuses > ./data/statuses.json
```

**更新を実行**
```bash
python -m backlog_tools.add_milestone_multi


python -m backlog_tools.delete_milestone_multi
```
