# Java Coding Interview Practice

国内大手Web企業のコーディング面接を想定した、Java + LeetCodeの学習リポジトリです。
期限復習を優先し、復習がなければ実力に合うEasyまたはMediumを1問推薦します。

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

`done` は評価と短い振り返りを対話形式で記録します。

| 評価 | 基準 |
|---|---|
| Again | 解答または直接的なヒントを参照した |
| Hard | 自力だが大幅に迷った、時間超過、重要な修正があった |
| Good | 目安時間内に自力実装し、計算量と境界値を説明できた |
| Easy | 素早く正確で、別解やトレードオフも説明できた |

計算量は長文不要です。次のような一行だけ残します。

```text
時間 O(n) / 空間 O(n) — HashSetに最大n件を保持するため
```

非対話で記録する場合:

```bash
python3 scripts/done.py 203 \
  --rating good --minutes 18 \
  --pattern "Linked List: sentinelで先頭削除を統一" \
  --complexity "時間 O(n) / 空間 O(1) — 1回走査のみ" \
  --lesson "末尾ではなくcurrent.nextを確認する"
```

## 難易度の決まり方

難易度は全体の問題数ではなく、面接頻出パターンごとに判断します。

- 確認済みEasyが2問未満、直近にAgain/Hardがある、または25分超ならEasy
- 異なるEasy 2問をGood以上・25分以内で解けたらMedium
- MediumでAgainが続けば同じパターンのEasyへ戻る
- 異なるMedium 3問をGood以上で解けたら、そのパターンは面接基礎定着

既存の履歴なしmastered問題は消去せず `unverified` として扱い、次の復習で現在の実力を確認します。

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

学習コマンドは自動でpull/commit/pushしません。同期したいときだけ実行します。

```bash
make sync
make sync M="progress: review linked list"
```

同期対象は解答・テスト・進捗・学習スクリプト・関連設定です。対象ファイルを表示し、確認後にcommit、pull --rebase、pushします。対象外のファイルや既にstage済みの変更は勝手に混ぜません。

## テスト

```bash
make test-scripts
mvn test
```

ローカルJUnitはタイポ、境界値、回帰の検出用です。最終的な正解判定にはLeetCode Acceptedを使います。
