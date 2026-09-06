# Source freeze

AuthorityEffect: None.

This manifest establishes source custody only, not the stopping conditions,
a theorem, independent discovery, or authority. Only comparison.md may be
added after this dedicated marker commit; defects it reveals remain OPEN.

```json
{
  "authority_effect": "None",
  "byte_domain": "Git blob bytes, not checkout line endings",
  "exclusions": [
    "FREEZE.md describes its parent; ignored generated files are not source"
  ],
  "files": [
    {
      "bytes": 138,
      "mode": "100644",
      "path": ".gitattributes",
      "sha256": "979d340f32618d42128a8792cba3f8026f4e1a3da10a60fdbc816dd8117a692f"
    },
    {
      "bytes": 62,
      "mode": "100644",
      "path": ".gitignore",
      "sha256": "71f142dba50ba79e2b4a0a92ae199a64063323a0b9a47d88f67e9d90828ad034"
    },
    {
      "bytes": 57686,
      "mode": "100644",
      "path": "MANUAL.md",
      "sha256": "d12400200f797521432b83a94175a3eff85462cdd0104d9f8e2e5652b3102c87"
    },
    {
      "bytes": 3036,
      "mode": "100644",
      "path": "PLAN.md",
      "sha256": "816d86cdbd9538786acf14ca1b00c943cb4fc63ec1dd47c6cc45b1596a1034e9"
    },
    {
      "bytes": 18776,
      "mode": "100644",
      "path": "SEED.md",
      "sha256": "ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be"
    },
    {
      "bytes": 2809,
      "mode": "100644",
      "path": "challenge0/PREDICTIONS.md",
      "sha256": "a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395"
    },
    {
      "bytes": 7463,
      "mode": "100644",
      "path": "challenge0/STATUS.md",
      "sha256": "c2a0975370384c22d95dff45380a66743146e34b5399bc6b65644c42269fceb6"
    },
    {
      "bytes": 6683,
      "mode": "100644",
      "path": "challenge1/PREDICTIONS.md",
      "sha256": "7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7"
    },
    {
      "bytes": 33680,
      "mode": "100644",
      "path": "challenge1/STATUS.md",
      "sha256": "681244b019de77f9932e1046b1b523b5d11fd9b5e63baecf0af085daf2816b23"
    },
    {
      "bytes": 8834,
      "mode": "100644",
      "path": "challenge2/PREDICTIONS.md",
      "sha256": "95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474"
    },
    {
      "bytes": 26233,
      "mode": "100644",
      "path": "challenge2/STATUS.md",
      "sha256": "93cc103ec8fb623d87f9baec1a11968a285a3c71120cf22579d7009654205d19"
    },
    {
      "bytes": 10220,
      "mode": "100644",
      "path": "challenge3/PREDICTIONS.md",
      "sha256": "27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755"
    },
    {
      "bytes": 29004,
      "mode": "100644",
      "path": "challenge3/STATUS.md",
      "sha256": "4c7e38b6cbb13e39c9dd0b839e66684e8d585d01a35568d2fcd4b120cf76f87d"
    },
    {
      "bytes": 10510,
      "mode": "100644",
      "path": "challenge4/PREDICTIONS.md",
      "sha256": "42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041"
    },
    {
      "bytes": 29813,
      "mode": "100644",
      "path": "challenge4/STATUS.md",
      "sha256": "1af6e6843d408740d7dce6d0fdd38fb1bed1f74519cd8a4c89e24c3afc377f02"
    },
    {
      "bytes": 10723,
      "mode": "100644",
      "path": "challenge5/PREDICTIONS.md",
      "sha256": "b3aab18d8e5a0700e563862ef7a884248badefbc7c653df0e00097044e3d99de"
    },
    {
      "bytes": 41922,
      "mode": "100644",
      "path": "challenge5/STATUS.md",
      "sha256": "5b2a9f44ddd5d8a12c03825791fac509c57a68ac6968205522cf86889e3d261d"
    },
    {
      "bytes": 125386,
      "mode": "100644",
      "path": "change_log.md",
      "sha256": "2ad2b98716580a5f64b038cad0bb5ed9f514af46f8ecc2986484f159f3024d4a"
    },
    {
      "bytes": 4081,
      "mode": "100644",
      "path": "check_coverage.py",
      "sha256": "1e5f63ead1683c90ec6dbcb0ed12c73a92b1e8b5d8cfdcdd46468462437a7165"
    },
    {
      "bytes": 197868,
      "mode": "100644",
      "path": "claim_ledger.md",
      "sha256": "cf2943054305bd205a4dd318e182fca3f13d77f27e60e4a7c4275ad75ae298a7"
    },
    {
      "bytes": 328,
      "mode": "100644",
      "path": "code/boundary/__init__.py",
      "sha256": "4f21376a01f702d7e98df1f329fda41a1b5e1fe6876d4c3e18d2b5e800fa604f"
    },
    {
      "bytes": 12063,
      "mode": "100644",
      "path": "code/boundary/challenge0.py",
      "sha256": "f33767e4429b5ef22d9cb417418747e86277944abcf8f864a0a722670c38aa5e"
    },
    {
      "bytes": 39339,
      "mode": "100644",
      "path": "code/boundary/challenge1.py",
      "sha256": "2dc50400adbd94bc517a36a9068e0261ce7c4266bc278dbe32fae885d687f486"
    },
    {
      "bytes": 40896,
      "mode": "100644",
      "path": "code/boundary/challenge2.py",
      "sha256": "e1ecf9fa114ded868db14e1ccf6bfb51965f6b7248b155dc085579b79aead8c7"
    },
    {
      "bytes": 67112,
      "mode": "100644",
      "path": "code/boundary/challenge3.py",
      "sha256": "dd28174bed8e37f160d53ee363dc16deee8ecb32d46713c029c57ea7197b5872"
    },
    {
      "bytes": 84730,
      "mode": "100644",
      "path": "code/boundary/challenge4.py",
      "sha256": "1f3832e1c98a50bb0052e84399a7cdcdc55d60372861fc2e2e76196a8d344c52"
    },
    {
      "bytes": 87142,
      "mode": "100644",
      "path": "code/boundary/challenge5.py",
      "sha256": "b54727b8e7e6b4eeff72fc0bd93f20a3b5a7f52421087023169d4d326d5ba052"
    },
    {
      "bytes": 76467,
      "mode": "100644",
      "path": "code/boundary/continuation1.py",
      "sha256": "0805b1d98678751ec4588f64e4cfc8676437a06a354e23b03eb6700d1a88e76d"
    },
    {
      "bytes": 21142,
      "mode": "100644",
      "path": "code/boundary/continuation2.py",
      "sha256": "e46f6b173cbf745b0761e5e923de26bcbf2b264aed152ceaa49965575a5d82f6"
    },
    {
      "bytes": 46947,
      "mode": "100644",
      "path": "code/boundary/model.py",
      "sha256": "6755b61b0aa1850bb077eb10a28b90ad0b9197410fa21b4e12705930a99b3618"
    },
    {
      "bytes": 13014,
      "mode": "100644",
      "path": "code/boundary/presentation.py",
      "sha256": "3df4c0ac07d168df5123afd0b527f287ff8ee75b8895d367256f691da78ca546"
    },
    {
      "bytes": 12417,
      "mode": "100644",
      "path": "continuation/stage1/PREDICTIONS.md",
      "sha256": "ac401dafbfa5072f04b6ab532992eae41391f87b6fe4441592b86804c4bf8313"
    },
    {
      "bytes": 41026,
      "mode": "100644",
      "path": "continuation/stage1/STATUS.md",
      "sha256": "29df067b3e4d508ac3baf6fe2ab89dd6c0490fadf465363c1c79645d023712e5"
    },
    {
      "bytes": 4024,
      "mode": "100644",
      "path": "continuation/stage2/PREDICTIONS.md",
      "sha256": "f4b3ebf85ad0176352647a606e8dd856674fb153d89e10e17d48f4734cf26f06"
    },
    {
      "bytes": 14127,
      "mode": "100644",
      "path": "continuation/stage2/STATUS.md",
      "sha256": "cc8ba1c34a792ef0e03c0d35cc0b6d5776f325b22d622a068f6e0a3a7017b397"
    },
    {
      "bytes": 11975,
      "mode": "100644",
      "path": "lean/BoundarySeed.lean",
      "sha256": "4efff86c331481f5e3fd4b1220e29ae7c5c2394dab99d9f9cef85ed020d4da58"
    },
    {
      "bytes": 6855,
      "mode": "100644",
      "path": "lean/BoundarySeed/Basic.lean",
      "sha256": "8cdbd4218168bbdcd7e5964fa1874b9e83022cf3fd6b110534b441139139aa4d"
    },
    {
      "bytes": 13940,
      "mode": "100644",
      "path": "lean/BoundarySeed/Challenge1.lean",
      "sha256": "e4142cab86510182aa7fe00490894625971a0df7ef48d04cfaa90056a302d349"
    },
    {
      "bytes": 9986,
      "mode": "100644",
      "path": "lean/BoundarySeed/Challenge2.lean",
      "sha256": "3115a890bc6449e00e7347779388e2dca287a787b99f7312a8a9b4161d1987de"
    },
    {
      "bytes": 9348,
      "mode": "100644",
      "path": "lean/BoundarySeed/Challenge3.lean",
      "sha256": "a1e82cf45da61d7f0d48e97cf0519c15b5df4e3d0a790b1684030024f95bfd2d"
    },
    {
      "bytes": 15012,
      "mode": "100644",
      "path": "lean/BoundarySeed/Challenge4.lean",
      "sha256": "c813f242244f3fdaabb5acbcc7c25a0966c21f6f7b2bfc10136f753ac076ab52"
    },
    {
      "bytes": 17308,
      "mode": "100644",
      "path": "lean/BoundarySeed/Challenge5.lean",
      "sha256": "4eeeba493b59ed881a4dcfc4957a510464cfd962bab6cb8cfd79c505095e2b48"
    },
    {
      "bytes": 9878,
      "mode": "100644",
      "path": "lean/BoundarySeed/Continuation1.lean",
      "sha256": "40c9979e43257675bc7aa2d8d5e7b61109e2aca1742ffdb2baa427c78d5721a5"
    },
    {
      "bytes": 3781,
      "mode": "100644",
      "path": "lean/BoundarySeed/Continuation2.lean",
      "sha256": "1716bbe27ee14616e49a158131099cbf8aeb3a849a88efb3b55f5a4180c0fb18"
    },
    {
      "bytes": 15595,
      "mode": "100644",
      "path": "lean/axioms.txt",
      "sha256": "1ac74545715f49841cd56e5ba91b1444d2495d4bdb16455efa3f858570f3b05c"
    },
    {
      "bytes": 144,
      "mode": "100644",
      "path": "lean/lake-manifest.json",
      "sha256": "0e83b52269e9f17e20f6a2d8acb466ccf589f5aabbd037b095e26d06744e09e4"
    },
    {
      "bytes": 110,
      "mode": "100644",
      "path": "lean/lakefile.toml",
      "sha256": "78a83533b4d0c4036f07559065b4dec49f69263b33d4d457f8ff547a316fe979"
    },
    {
      "bytes": 25,
      "mode": "100644",
      "path": "lean/lean-toolchain",
      "sha256": "302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b"
    },
    {
      "bytes": 275214,
      "mode": "100644",
      "path": "paper.md",
      "sha256": "e74e1c7ef6d4ee7e3e94e34d9cb6a07f7c1f66f09fe9cfab0b2921a823a96273"
    },
    {
      "bytes": 686,
      "mode": "100644",
      "path": "pyproject.toml",
      "sha256": "72d9d1a57cbe23c64552fc39722ed5d76fb430d12b60adc22ea99e07a1438f83"
    },
    {
      "bytes": 5553,
      "mode": "100644",
      "path": "receipts/challenge0.json",
      "sha256": "7441796b52658c72698774565cbef69aa4b17740d90ba5bb2c27e23c7aafb7c9"
    },
    {
      "bytes": 28363,
      "mode": "100644",
      "path": "receipts/challenge1.json",
      "sha256": "de48399f3fe54792edf8294b72fe92768f3d25b7144589f65d3d7ec45a0eb1b6"
    },
    {
      "bytes": 35499,
      "mode": "100644",
      "path": "receipts/challenge2.json",
      "sha256": "ca6a9f935951b7d813baf9ddbea881c32325f2e6b5309780a333477f13f4b12b"
    },
    {
      "bytes": 220518,
      "mode": "100644",
      "path": "receipts/challenge3.json",
      "sha256": "e4904075aaa07dd05a2f9d0cba313e77b6eb965a44efecb5cff51864f70a64ab"
    },
    {
      "bytes": 795960,
      "mode": "100644",
      "path": "receipts/challenge4.json",
      "sha256": "0e6bf1d1c7f0d5c61f12ca0bb1e4e3bbff556219680c7873aefc78e5b095704d"
    },
    {
      "bytes": 128086,
      "mode": "100644",
      "path": "receipts/challenge5.json",
      "sha256": "0c4d04e5a35eea235e05513c984820abd5d11179b6915ecbe3c0a4df5d27e716"
    },
    {
      "bytes": 212629,
      "mode": "100644",
      "path": "receipts/continuation1.json",
      "sha256": "2b135b76b6558198adf59a46f4b498ac30aa139444a35108c0a21de2c8ce9697"
    },
    {
      "bytes": 349533,
      "mode": "100644",
      "path": "receipts/continuation2.json",
      "sha256": "40f97c814badfdccb41c9b2f4be93a876e1b62283a6579c8cb26876324c0d6e8"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge0.py",
      "sha256": "c85a59a1e3f2cb3e1a7ef77fc0d093de0ef11edbabceb980fac841ec25791bd3"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge1.py",
      "sha256": "e24e37ebe21109fe6c61c8c40395e09dbfdda7fbd574b7de38fc6fedafc4b58d"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge2.py",
      "sha256": "2ab3985ef02bbc9d0d4187fe82906d1476504d40985e7bead33b269b163ea236"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge3.py",
      "sha256": "a03b764fd99702d9a047aabcbaf15a76725367c13b68bc24a4a97ffb29fca9f4"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge4.py",
      "sha256": "31c34f0b2dbbb3425d019b9ded4571d72e788b2699543313f7573d16ebdfc9c1"
    },
    {
      "bytes": 855,
      "mode": "100644",
      "path": "run_challenge5.py",
      "sha256": "a7b162801547ad01f948c19df6294ed88a0da5b1db29b9900ac4fb1b154ea641"
    },
    {
      "bytes": 870,
      "mode": "100644",
      "path": "run_continuation1.py",
      "sha256": "fb5ec0f3b843a72c4411a9a71a6a65258d5e98d464c5eea13e3bc0fd26722fcf"
    },
    {
      "bytes": 693,
      "mode": "100644",
      "path": "run_continuation2.py",
      "sha256": "f32665c9ab0da283fa1f17422b96d102f7fb13908bbc36fca3cd0ee6e3b252e3"
    },
    {
      "bytes": 13790,
      "mode": "100644",
      "path": "tests/test_blind.py",
      "sha256": "354457f0b26d3a2a0fd4347839d529c5bf7dd4f6bb7d506898b82f4c000aa818"
    },
    {
      "bytes": 8083,
      "mode": "100644",
      "path": "tests/test_challenge0.py",
      "sha256": "bada38970139d699d6a7c3ec954ae3a40a27085d7d8414a464f7121cfa0bfc4c"
    },
    {
      "bytes": 40149,
      "mode": "100644",
      "path": "tests/test_challenge1.py",
      "sha256": "c465b66c7cd90a1d71f0a2f9d0e180198f12c184707790b576b97ebdcef70fe0"
    },
    {
      "bytes": 32152,
      "mode": "100644",
      "path": "tests/test_challenge2.py",
      "sha256": "41f69e4a02d10fe33203162b629719e9dc0d521aba2e504e6ee2fd152500bd5b"
    },
    {
      "bytes": 42994,
      "mode": "100644",
      "path": "tests/test_challenge3.py",
      "sha256": "59d9e3935f4f9e61c593fd2278a0d5fe90f1057f3c03e596f1d7e52f25766114"
    },
    {
      "bytes": 56087,
      "mode": "100644",
      "path": "tests/test_challenge4.py",
      "sha256": "4611f6517468d1310588f49fb83b7c225df99f9bff21924f629dc36888b74296"
    },
    {
      "bytes": 63998,
      "mode": "100644",
      "path": "tests/test_challenge5.py",
      "sha256": "8adf37710c03ffe013881c98376825e45206ef911d653a60187fa80d3246335d"
    },
    {
      "bytes": 44856,
      "mode": "100644",
      "path": "tests/test_continuation1.py",
      "sha256": "1a1bc493b9f5ac379555dd9b7a8e6e6fc43fbb2631767c20180511cb1af50bd9"
    },
    {
      "bytes": 19286,
      "mode": "100644",
      "path": "tests/test_continuation2.py",
      "sha256": "b44e40fce61757d904cd43b75858ce44df207ed233c397df67641cbf009030c0"
    },
    {
      "bytes": 991,
      "mode": "100644",
      "path": "tests/test_coverage_gate.py",
      "sha256": "7de0e92476287e9d96c65d24b61d7c42a72b7d51c04697e13b3bcc91d4bc4a8d"
    },
    {
      "bytes": 15613,
      "mode": "100644",
      "path": "tests/test_freeze.py",
      "sha256": "fa8c7c785f38b286f394cde8b059f597ab52b6b98054784c2efe983e9471af82"
    },
    {
      "bytes": 4789,
      "mode": "100644",
      "path": "tests/test_lean_gate.py",
      "sha256": "400dcdd00835b99a5d07abcb96755d8993844b0bc68e34ecb36505e045e16cae"
    },
    {
      "bytes": 26850,
      "mode": "100644",
      "path": "tests/test_model.py",
      "sha256": "243eb16670766f5db006f47ab0b5a0271f9ccafbaa27d2455a55a0abd1b2aadd"
    },
    {
      "bytes": 3552,
      "mode": "100644",
      "path": "tests/test_presentation.py",
      "sha256": "e122fdb31e07c2cb841f30cea0d6eeafb9aac134acd1329b8fb3c710899627fa"
    },
    {
      "bytes": 5777,
      "mode": "100644",
      "path": "tests/test_prose_citations.py",
      "sha256": "6508daf3e4db79822bd707a8a2cd1a7d49e52121a20d36fea639f21b84abd865"
    },
    {
      "bytes": 15595,
      "mode": "100644",
      "path": "verify_freeze.py",
      "sha256": "5972deeff5e0fceb69cafe42cbf537a7c4eb2b65f910a1f91dcf040f477da8ef"
    },
    {
      "bytes": 7980,
      "mode": "100644",
      "path": "verify_lean.py",
      "sha256": "1ec8e85052547507f42e266f8588b6782e2d99042e29daea49893f4ba14f79db"
    },
    {
      "bytes": 5839,
      "mode": "100644",
      "path": "verify_pins.py",
      "sha256": "e590988b4867b9ab851c476bb1577d3bbd8c989f56836526aa8b53a4eacb338e"
    }
  ],
  "schema": "boundary-source-freeze-v1",
  "source_commit": "5cfdb23250a8d63c44e1fdb05bcad8567036d18e",
  "write_root": "research/boundary_seed"
}
```
