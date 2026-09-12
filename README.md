# Java Problem Pattern Practice

Java + LeetCodeで、問題パターンごとの解法を身につけるための学習リポジトリです。
期限復習を優先し、復習がなければ実力に合う難易度の問題を1問推薦します。

## 最初に

Java 17以上とMavenが必要です。環境を確認してください。

```bash
make doctor
```

## 毎日の流れ

```bash
make today
```

表示された期限復習は原則すべて消化します。復習がなければ新規問題は1問だけです。
当日の評価を記録し、期限復習と未完了問題がなくなったら学習終了です。
その日の `make today`・`make next`・`make recommend` は追加の新規問題を勧めません。
翌日は、期限復習と未完了問題がなければ新規問題を推薦します。

### 復習

```bash
make review N=203
# 過去コードを見ずに解く → LeetCodeへSubmit
make done N=203
```

### 新規問題

```bash
make recommend
make new N=3
# 解く → LeetCodeへSubmit
make done N=3
```

Easyは20〜25分、Mediumは35〜40分を目安にします。実装前に次を声に出します。

1. 入出力、制約、境界値
2. 素朴な解法と改善案
3. 採用するデータ構造と理由

## 4段階評価

`done` は評価を対話形式で記録します。

| 評価 | 基準 |
|---|---|
| Again | 解答または直接的なヒントを参照した |
| Hard | 自力だが大幅に迷った、または重要な修正があった |
| Good | 自力で正しく実装できた |
| Easy | 迷わず正確に実装できた |

非対話で記録する場合:

```bash
python3 scripts/done.py 203 --rating good
```

## 難易度の決まり方

難易度は全体の問題数ではなく、問題パターンごとに判断します。

- 確認済みEasyが2問未満、または直近にAgain/HardがあればEasy
- 異なるEasy 2問をGood以上で解けたらMedium
- MediumでAgainが続けば同じパターンのEasyへ戻る
- 異なるMedium 3問をGood以上で解けたら、そのパターンは基礎定着
- 確認済みMediumが5問以上、リトライ率30%以下、直近3回がGood以上ならHard

リトライ率は、その問題パターンの直近10回の評価に占めるAgainの割合です。
10回未満なら記録されている評価を使い、履歴がない問題は分母に含めません。
累計Again回数は履歴として残しますが、難易度の判定には使いません。

既存の履歴なしmastered問題は消去せず `unverified` として扱い、次の復習で現在の実力を確認します。
新しい評価には時刻も記録し、同日の評価を新しい順に集計します。
日付だけの旧履歴も利用できますが、同日の異なる問題間の評価順は復元できません。

## 間隔反復

| stage | 基準間隔 |
|---|---:|
| 0 | 1日 |
| 1 | 3日 |
| 2 | 7日 |
| 3 | 21日 |
| 4 | 60日 |
| 5 | 180日 |

Againはstage 0、Hardは1段階下降、Goodは1段階上昇、Easyは2段階上昇です。
stage 2以降は復習が同日に集中しないよう、基準日の前後で負荷分散します。

## Git同期

`done` で評価を記録すると、その問題の `Solution.java`、`SolutionTest.java` と
`progress.json` を自動でcommit、pushします。
同期に失敗しても評価は保存済みです。同じ日に `make done N=203` を再実行すると、
評価や復習日程を変更せず、その問題の同期だけを再試行します。
別の日に同期を再試行する場合は、明示的に指定してください。

```bash
python3 scripts/done.py 203 --sync-only
```

同じ日に実際に解き直して別の評価を追加したい場合は、
`python3 scripts/done.py 203 --new-attempt` を使います。

ほかの学習スクリプトや設定も同期したい場合は、次を実行します。

```bash
make sync
make sync M="progress: review linked list"
```

`make sync` の同期対象は解答・テスト・進捗・学習スクリプト・関連設定です。対象ファイルを表示し、確認後にcommit、pull --rebase、pushします。対象外のファイルや既にstage済みの変更は勝手に混ぜません。
ファイル変更がなくても、確認後にpull・pushして未送信のcommitを同期します。

## テスト

```bash
make test-scripts
mvn test
```

ローカルJUnitはタイポ、境界値、回帰の検出用です。最終的な正解判定にはLeetCode Acceptedを使います。
