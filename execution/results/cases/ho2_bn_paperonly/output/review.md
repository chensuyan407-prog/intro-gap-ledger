# Review - ho2_bn_paperonly

status: **success** - introduction + related work written: 4 parts, 7 references, source map for 15 sentences; quality checks flagged 0 issue(s) and 4 warning(s) (quality_issues / review.md); 17 item(s) for author confirmation (needs_review)

summary: {"sentences": 15, "cited_sentences": 9, "author_judgments": 2, "references": 7, "groups": 2, "gaps": 1, "contributions": 3, "fails": 0, "warns": 4}

## warn (4)

- S5d P2.S1: cross-lingual citation [@sutskever2013] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 这一路线不改变各层输入的分布，而是改变参数更新方式或减轻激活饱和。
- S5d P2.S1: cross-lingual citation [@nair2010] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 这一路线不改变各层输入的分布，而是改变参数更新方式或减轻激活饱和。
- S5d P3.S1: cross-lingual citation [@lecun1998a] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 另一条路线直接规范输入的分布，区别在于统计量在哪里计算。
- S5d P3.S1: cross-lingual citation [@lyu2008] without an explicit #evidence id: lexical matching is not possible, add the id of the supporting sentence  
  > 另一条路线直接规范输入的分布，区别在于统计量在哪里计算。

## Needs human confirmation

- secondary_evidence sutskever2013: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list sutskever2013: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence duchi2011: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list duchi2011: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence nair2010: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list nair2010: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence bengio2010: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list bengio2010: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence lecun1998a: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list lecun1998a: record parsed from the printed reference list of the own paper; confirm fields
- secondary_evidence lyu2008: checked against citing_context (how the own paper / notes describe it), not against the original work
- metadata_from_reference_list lyu2008: record parsed from the printed reference list of the own paper; confirm fields
- claim_unverifiable wiesler2011: no source text: the statement about this work was checked against metadata only
- metadata_from_reference_list wiesler2011: record parsed from the printed reference list of the own paper; confirm fields
- author_note : 本案例只有论文本身：所有对他人工作的转述都基于论文正文中的引用句（二级证据），参考文献表由论文印刷版解析得到，需核对作者、题名与出处。
- author_judgment P1.S2: 然而，训练深层网络时每一层的输入分布会随前面各层参数的变化而改变，这使训练需要较小的学习率和仔细的参数初始化。
- author_judgment P2.S4: 两类方法都没有直接控制中间层输入的分布。

## Uncertainty

- statements about wiesler2011 rest on library metadata only (no source text provided)
- 1 input parse problem(s): see parse_problems
- support scores are lexical; semantic faithfulness of paraphrases was judged by the agent, not proven by the script
