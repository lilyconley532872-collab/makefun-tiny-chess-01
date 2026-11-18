# tiny-chess-01 — PeSTO engine (fix)

`main.py` (4,011 bytes, packed with `makefun compress` from the readable
source) plays every game through the env with a real search: a PeSTO
tapered evaluation (Texel-tuned middlegame/endgame piece-square tables,
computed incrementally) plus principal variation search with late-move
reductions, killers, a Zobrist-hash transposition table, null-move
pruning, quiescence and check extensions. Default budget 100,000 nodes
(~4 s/move, under the 10 s limit). Standard library only.

## The size rule

- `main.py` is the whole engine: at most 4,096 bytes as committed,
  Python 3.13, standard library only. It reads, imports or execs no other
  file in the repository.
- Every byte counts: comments, whitespace, docstrings.
- Compression is allowed and counted. A `main.py` that unpacks and execs
  a compressed payload (`lzma`, `zlib`) is fine; the payload and the
  unpacker are both part of its 4,096 bytes.
- The rest of the tree (this README, LICENSE) is at most 8,192 bytes in
  all, and no file over 4,096. MIT, BSD, ISC and 0BSD licences fit.
- Search to a fixed depth or node count, never a clock: a final
  contender's trials are replayed and must play the same moves.

## Grade it locally

Practice trials (local, kit scorer): trial-0 Elo 1809 (5W/1D/0L),
trial-1 Elo 2112 capped (6W/0D/0L), trial-2 Elo 1364–1654; mean 1858 at
100k nodes. Round-1 entry scored Elo 1550 on the leaderboard; this fix
is decisively stronger (head-to-head vs the old engine: 4/4 wins).

You need Docker and the `makefun` CLI. Download the competition's dev
kit, unpack it, and from inside it run:

    makefun grade-local --kit . --bot <your repository> --driver docker

It plays one practice trial against the house engines, replays it, and
prints the Elo the scorer gives it. Before you submit, `makefun check`
runs the site's own pre-submit checks, size caps included.
