# bpe_demo.py —— 50 行手写 BPE 训练 + 编码，理解子词是怎么"长出来"的
# 运行：python3 bpe_demo.py
from collections import Counter


def get_pairs(word_freqs):
    """统计所有相邻符号对的频率。word 用元组表示，如 ('l','o','w','</w>')。"""
    pairs = Counter()
    for word, freq in word_freqs.items():
        for i in range(len(word) - 1):
            pairs[(word[i], word[i + 1])] += freq
    return pairs


def merge_pair(pair, word_freqs):
    """把 word_freqs 中所有出现的 pair 合并成一个新符号。"""
    merged = Counter()
    bigram = pair
    for word, freq in word_freqs.items():
        new_word, i = [], 0
        while i < len(word):
            # 找到 pair 的起点
            if i < len(word) - 1 and (word[i], word[i + 1]) == bigram:
                new_word.append(word[i] + word[i + 1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        merged[tuple(new_word)] = freq
    return merged


def train_bpe(corpus, num_merges):
    """训练 BPE：反复找最高频的相邻对并合并。"""
    # 初始切分：按字符切，词尾加 </w> 表示结束
    word_freqs = Counter()
    for word, freq in corpus.items():
        word_freqs[tuple(list(word) + ["</w>"])] = freq

    merges = []  # 记录合并顺序，编码时要按同样顺序应用
    for step in range(num_merges):
        pairs = get_pairs(word_freqs)
        if not pairs:
            break
        best = pairs.most_common(1)[0][0]
        word_freqs = merge_pair(best, word_freqs)
        merges.append(best)
        print(f"第 {step + 1} 次合并: {best[0]} + {best[1]} -> {best[0] + best[1]}"
              f"  (频次 {pairs[best]})")
    return merges, word_freqs


def encode(word, merges):
    """按训练时的合并顺序，把新词编码成子词序列。"""
    symbols = list(word) + ["</w>"]
    for a, b in merges:  # 严格按合并顺序应用
        out, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        symbols = out
    return symbols


if __name__ == "__main__":
    # 一份迷你语料：词 -> 出现次数
    corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3, "newer": 2}
    merges, final = train_bpe(corpus, num_merges=8)

    print("\n=== 训练后的词表切分 ===")
    for word, freq in sorted(final.items(), key=lambda x: -x[1]):
        print(f"{''.join(word):<16} 频次={freq}  子词={word}")

    print("\n=== 用学到的合并规则编码新词（验证 OOV 能力）===")
    for w in ["lowest", "slowest", "newest"]:
        print(f"{w:<10} -> {encode(w, merges)}")