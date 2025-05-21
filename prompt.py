TYPE1_2HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into two sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included.", "#2"]
}}
```

Example:
Question: When was the institute that owned The Collegian founded?
Tips:
```json
{{
    "Q1": ["The Collegian >> owned by", "#1"],
    "Q2": ["When was #1 founded?", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Which institute owned The Collegian?", "#1"],
    "Q2": ["When was #1 founded?", "#2"]
}}
```

Question: What city is the person who broadened the doctrine of philosophy of language from?
Tips:
```json
{{
    "Q1": ["who broadened the doctrine of philosophy of language", "#1"],
    "Q2": ["What city is #1 from?", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Who broadened the doctrine of philosophy of language?", "#1"],
    "Q2": ["What city is #1 from?", "#2"]
}}
```

Question: What language was used by Renana Jhabvala's mother?
Tips:
```json
{{
    "Q1": ["Who was Renana Jhabvala's mother?", "#1"],
    "Q2": ["#1 >> languages spoken, written or signed", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Who was Renana Jhabvala's mother?", "#1"],
    "Q2": ["What language was used by #1?", "#2"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE1_2HOP_BRIDGE_FOR_HOTPOTQA_SYSTEM_PROMPT = """Given a bridge question. A bridge question involves two facts that are connected by an intermediate entity.
Your job is to decompose the bridge question into two sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Output is not allowed to leak any factual information from the tips.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included.", "#2"]
}}
```

Example:
Question: When was the institute that owned The Collegian founded?
Tips:
    1. The Collegian (Houston Baptist University): The Collegian is the bi-weekly official student publication of Houston Baptist University in Houston, Texas.
    2. Houston: Houston Baptist University, affiliated with the Baptist General Convention of Texas, offers bachelor's and graduate degrees. It was founded in 1960 and is located in the Sharpstown area in Southwest Houston.
Output:
```json
{{
    "Q1": ["Which institute owned The Collegian?", "#1"],
    "Q2": ["When was #1 founded?", "#2"]
}}
```

Question: What city is the person who broadened the doctrine of philosophy of language from?
Tips:
    1. Philosophy of language: In the early 19th century, the Danish philosopher S\u00f8ren Kierkegaard insisted that language ought to play a larger role in Western philosophy.
    2. S\u00f8ren Kierkegaard: Kierkegaard was born to an affluent family in Copenhagen. His mother, Ane S\u00f8rensdatter Lund Kierkegaard, had served as a maid in the household before marrying his father, Michael Pedersen Kierkegaard.
Output:
```json
{{
    "Q1": ["Who broadened the doctrine of philosophy of language?", "#1"],
    "Q2": ["What city is #1 from?", "#2"]
}}
```

Question: What language was used by Renana Jhabvala's mother?
Tips:
    1. Renana Jhabvala: Renana Jhabvala was born in Delhi to the Booker Prize winning novelist and screen-writer, Ruth Prawer Jhabvala, and well-known architect Cyrus S. H. Jhabvala. Her grandparents were active in public life during the early to mid part of the twentieth century.
    2. The Householder (novel): The Householder is a 1960 English language novel by Ruth Prawer Jhabvala. It is about a young man named Prem who has recently moved from the first stage of his life, a student, to the second stage of his life, a householder.
Output:
```json
{{
    "Q1": ["Who was Renana Jhabvala's mother?", "#1"],
    "Q2": ["What language was used by #1?", "#2"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE2_2HOP_COMPARISON_SYSTEM_PROMPT = """Your job is to decompose the question into two sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language.", "#1"],
    "Q2": ["A sub-question described in natural language.", "#2"]
}}
```

Example:
Question: Which film came out first, The Love Route or Engal Aasan?
Tips:
```json
{{
    "Q1": ["The Love Route >> publication date", "#1"],
    "Q2": ["Engal Aasan >> publication date", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["What is the publication date of The Love Route?", "#1"],
    "Q2": ["What is the publication date of Engal Aasan?", "#2"]
}}
```

Question: Who was born first, Terrell Brandon or Greg Brezina?
Tips:
```json
{{
    "Q1": ["Terrell Brandon >> date of birth", "#1"],
    "Q2": ["Greg Brezina >> date of birth", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["When was Terrell Brandon born?", "#1"],
    "Q2": ["When was Greg Brezina born?", "#2"]
}}
```

Question: Are Harper High School (Chicago) and Santa Sabina College located in the same country?
Tips:
```json
{{
    "Q1": ["Santa Sabina College >> country", "#1"], 
    "Q2": ["Harper High School (Chicago) >> country", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["What country is Santa Sabina College located in?", "#1"],
    "Q2": ["What country is Harper High School (Chicago) located in?", "#2"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE2_2HOP_COMPARISON_FOR_HOTPOTQA_SYSTEM_PROMPT = """Given a comparison question. A comparison question involves comparing two independent facts.
Your job is to decompose the comparison question into two sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Output is not allowed to leak any factual information from the tips.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language.", "#1"],
    "Q2": ["A sub-question described in natural language.", "#2"]
}}
```

Example:
Question: Which film came out first, The Love Route or Engal Aasan?
Tips:
    1. The Love Route: The Love Route is a 1915 American Western silent film directed and written by Allan Dwan based upon a play by Edward Henry Peple.
    2. Engal Aasan: Engal Aasan is a 2009 Tamil action comedy- drama film directed by R. K. Kalaimani.
Output:
```json
{{
    "Q1": ["What is the publication date of The Love Route?", "#1"],
    "Q2": ["What is the publication date of Engal Aasan?", "#2"]
}}
```

Question: Who was born first, Terrell Brandon or Greg Brezina?
Tips:
    1. Terrell Brandon: Thomas Terrell Brandon( born May 20, 1970) is an American retired professional basketball player.
    2. Greg Brezina: Gregory Brezina( born January 7, 1946) is a former American football linebacker who played twelve seasons in the National Football League for the Atlanta Falcons.
Output:
```json
{{
    "Q1": ["When was Terrell Brandon born?", "#1"],
    "Q2": ["When was Greg Brezina born?", "#2"]
}}
```

Question: Are Harper High School (Chicago) and Santa Sabina College located in the same country?
Tips:
    1. Santa Sabina College: Located on multiple sites in Strathfield, an inner- western suburb of Sydney; and in, in the Southern Highlands of New South Wales, Australia; students are educated in the Dominican tradition.
    2. Harper High School (Chicago): William Rainey Harper High School( commonly known as Harper High School) is a public 4 \u2013 year high school located in the West Englewood neighborhood on the south side of Chicago, Illinois, United States.
Output:
```json
{{
    "Q1": ["What country is Santa Sabina College located in?", "#1"],
    "Q2": ["What country is Harper High School (Chicago) located in?", "#2"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE3_2HOP_INFERENCE_SYSTEM_PROMPT = """Your job is to decompose the question into two sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included.", "#2"]
}}
```

Example:
Question: Who is Rhescuporis I (Odrysian)'s paternal grandfather?
Tips:
```json
{{
    "Q1": ["Rhescuporis I >> father", "#1"],
    "Q2": ["#1 >> father", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Who was the father of Rhescuporis I (Odrysian)?", "#1"],
    "Q2": ["Who was the father of #1?", "#2"]
}}
```

Question: Who is Sobe (Sister Of Saint Anne)'s child-in-law?
Tips:
```json
{{
    "Q1": ["Sobe >> child", "#1"], 
    "Q2": ["#1 >> spouse", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Who is the child of Sobe (Sister Of Saint Anne)?", "#1"],
    "Q2": ["Who is the spouse of #1?", "#2"]
}}
```

Question: Where did Christian Ehrenfried Weigel graduate from?
Tips:
```json
{{
    "Q1": ["Christian Ehrenfried Weigel >> doctoral advisor", "#1"],
    "Q2": ["Johann Christian Polycarp Erxleben >> employer", "#2"]
}}
```
Output:
```json
{{
    "Q1": ["Who was Christian Ehrenfried Weigel's doctoral advisor?", "#1"],
    "Q2": ["Where did #1 work?", "#2"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE4_3HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into three sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language and the placeholder #2 must be included.", "#3"]
}}
```

Example:
Question: Who founded the college where the author of An Oxford University Chest was educated?
Tips:
```json
{{
    "Q1": ["An Oxford University Chest >> author", "#1"],
    "Q2": ["#1 >> educated at", "#2"],
    "Q3": ["#2 >> founded by", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["Who is the author of An Oxford University Chest?", "#1"],
    "Q2": ["Where was #1 educated?", "#2"],
    "Q3": ["Who founded #2?", "#3"]
}}
```

Question: Who was the spouse of the first president who identified as a member of Barack Obama's party in 2008?
Tips:
```json
{{
    "Q1": ["What party did Barack Obama belong to in 2008?", "#1"],
    "Q2": ["who was the first president identified as a #1", "#2"],
    "Q3": ["#2 >> spouse", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["What party did Barack Obama belong to in 2008?", "#1"],
    "Q2": ["Who was the first president who identified as a member of #1?", "#2"],
    "Q3": ["Who was the spouse of #2?", "#3"]
}}
```

Question: What county shares a border with the county that Jackson Township's county shares a border with?
Tips:
```json
{{
    "Q1": ["Jackson Township >> located in the administrative territorial entity", "#1"],
    "Q2": ["#1 >> shares border with", "#2"],
    "Q3": ["#2 >> shares border with", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["What county is Jackson Township located in?", "#1"],
    "Q2": ["What county shares a border with #1?", "#2"],
    "Q3": ["What county shares a border with #2?", "#3"]
}}
```


NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE5_3HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into three sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language and the placeholder #1 and #2 must be included.", "#3"]
}}
```

Example:
Question: What country includes the county bordering Barry county, that also includes the community of Logan, in the state where Houck Stadium is located?
Tips:
```json
{{
    "Q1": ["Barry County >> shares border with", "#1"],
    "Q2": ["Houck Stadium >> located in the administrative territorial entity", "#2"],
    "Q3": ["Logan, #1 , #2 >> country", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["Which county borders Barry County?", "#1"],
    "Q2": ["Where is Houck Stadium located?", "#2"],
    "Q3": ["Which country includes both Logan and #1, and is in #2?", "#3"]
}}
```

Question: What followed the last person to live in Versailles in the country that became allies with America after the battle of Saratoga?
Tips:
```json
{{
    "Q1": ["who became allies with america after the battle of saratoga", "#1"],
    "Q2": ["who was the last person to live in versaille", "#2"],
    "Q3": ["#2 of #1 >> followed by", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["Who became allies with America after the Battle of Saratoga?", "#1"],
    "Q2": ["Who was the last person to live in Versailles?", "#2"],
    "Q3": ["What followed #2 in #1?", "#3"]
}}
```

Question: How many of the people who sent families of deserters to concentration camps live in the country who won the 2002 World Cup in Japan?
Tips:
```json
{{
    "Q1": ["Who sent deserters families to concentration camps?", "#1"],
    "Q2": ["who won the 2002 world cup in japan", "#2"],
    "Q3": ["How many #1 live in #2 ?", "#3"]
}}
```
Output:
```json
{{
    "Q1": ["Who sent families of deserters to concentration camps?", "#1"],
    "Q2": ["Who won the 2002 World Cup in Japan?", "#2"],
    "Q3": ["How many of #1 live in #2?", "#3"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE6_4HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into four sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language and the placeholder #2 must be included. You can't start with 'When'.", "#3"],
    "Q4": ["A sub-question described in natural language and the placeholder #3 must be included.", "#4"]
}}
```

Example:
Question: Where is the lowest place in the country which, along with Eisenhower's VP's country, recognized Gaddafi's government early on?
Tips:
```json
{{
    "Q1": ["Who served as Eisenhower's vice president?", "#1"],
    "Q2": ["#1 was a president of what country?", "#2"],
    "Q3": ["Along with the #2 , what major power recognized Gaddafi's government at an early date?", "#3"],
    "Q4": ["where is the lowest place in the #3", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Who served as Eisenhower's vice president?", "#1"],
    "Q2": ["What country was #1 president of?", "#2"],
    "Q3": ["Which major power, along with #2, recognized Gaddafi's government early on?", "#3"],
    "Q4": ["Where is the lowest place in #3?", "#4"]
}}
```

Question: Who was the father of the person who led the first expedition to reach Asia by sailing west across the body of water Motuloa is located?
Tips:
```json
{{
    "Q1": ["Motuloa >> part of", "#1"],
    "Q2": ["#1 >> located in or next to body of water", "#2"],
    "Q3": ["who led the first expedition to reach asia by sailing west across #2", "#3"],
    "Q4": ["Who fathered #3 ?", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["What is Motuloa part of?", "#1"],
    "Q2": ["Where is #1 located in or next to a body of water?", "#2"],
    "Q3": ["Who led the first expedition to reach Asia by sailing west across #2?", "#3"],
    "Q4": ["Who was the father of #3?", "#4"]
}}
```

Question: In which country is International College in the city where the creator of paintings named for the country Iraq invaded in 1990 was born?
Tips:
```json
{{
    "Q1": ["Which country did Iraq invade in 1990?", "#1"],
    "Q2": ["#1 >> creator", "#2"],
    "Q3": ["#2 >> place of birth", "#3"],
    "Q4": ["International College, #3 >> country", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Which country did Iraq invade in 1990?", "#1"],
    "Q2": ["Who created paintings named for #1?", "#2"],
    "Q3": ["Where was #2 born?", "#3"],
    "Q4": ["What country is International College in #3 located in?", "#4"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE7_4HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into four sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language and the placeholder #1 and #2 must be included. You can't start with 'When'.", "#3"],
    "Q4": ["A sub-question described in natural language and the placeholder #3 must be included", "#4"]
}}
```

Examples:
Question: What is the size in square miles of the nation that has provided the most legal immigrants to where Gotham was filmed in the place Turks and Caicos is located?
Tips:
```json
{{
    "Q1": ["where is the tv show gotham filmed at", "#1"], 
    "Q2": ["Turks and Caicos Islands >> located on terrain feature", "#2"], 
    "Q3": ["What nation provided the most legal immigrants to #1 in the #2 ?", "#3"], 
    "Q4": ["what is the size of #3 in square miles", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Where was the TV show Gotham filmed?", "#1"],
    "Q2": ["What terrain feature is Turks and Caicos Islands located on?", "#2"],
    "Q3": ["What nation provided the most legal immigrants to #1 in #2?", "#3"],
    "Q4": ["What is the size of #3 in square miles?", "#4"]
}}
```

Question: Who broadcast the evening news TV show about the continent of the country where government phonology is popular and the country where the Dutch reform church comes from?
Tips:
```json
{{
    "Q1": ["Where is government phonology popular?", "#1"], 
    "Q2": ["where does the dutch reformed church come from", "#2"], 
    "Q3": ["#1 of the #2 >> continent", "#3"], 
    "Q4": ["#3 Tonight >> original broadcaster", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Where is government phonology popular?", "#1"],
    "Q2": ["Where does the Dutch Reformed Church come from?", "#2"],
    "Q3": ["What continent is #1 of the #2 located on?", "#3"],
    "Q4": ["Who originally broadcast the #3 Tonight news show?", "#4"]
}}
```

Question: Federal Senate of the country being the colonial holding in the continent having Aruba governed by the country having Prazeres is a part of what?
Tips:
```json
{{
    "Q1": ["Aruba >> continent", "#1"], 
    "Q2": ["Prazeres >> country", "#2"], 
    "Q3": ["what was the colonial holding in #1 that was governed by #2", "#3"], 
    "Q4": ["Federal Senate of #3 >> part of", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["What continent is Aruba located on?", "#1"],
    "Q2": ["What country is Prazeres in?", "#2"],
    "Q3": ["What was the colonial holding in #1 governed by #2?", "#3"],
    "Q4": ["What is the Federal Senate of #3 a part of?", "#4"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE8_4HOP_BRIDGE_SYSTEM_PROMPT = """Your job is to decompose the question into four sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language and the placeholder #1 must be included. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language. You can't start with 'When'.", "#3"],
    "Q4": ["A sub-question described in natural language and the placeholder #2 and #3 must be included.", "#4"]
}}
```

Examples:
Question: When did the capital of Virginia moved from John Nicholas's birth city to Charles Oakley's alma mater's city?
Tips:
```json
{{
    "Q1": ["Charles Oakley >> educated at", "#1"], 
    "Q2": ["#1 >> located in the administrative territorial entity", "#2"], 
    "Q3": ["John Nicholas >> place of birth", "#3"], 
    "Q4": ["when did the capital of virginia moved from #3 to #2", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Where was Charles Oakley educated?", "#1"],
    "Q2": ["Where is #1 located?", "#2"],
    "Q3": ["Where was John Nicholas born?", "#3"],
    "Q4": ["When did the capital of Virginia move from #3 to #2?", "#4"]
}}
```

Question: What weekly publication in the city where Steven Segaloff died is issued by the school attended by the author of America-Lite: How Imperial Academia Dismantled Our Culture?
Tips:
```json
{{
    "Q1": ["America-Lite: How Imperial Academia Dismantled Our Culture >> author", "#1"], 
    "Q2": ["#1 >> educated at", "#2"], 
    "Q3": ["Steven Segaloff >> place of birth", "#3"], 
    "Q4": ["What weekly publication in #3 is issued by #2 ?", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Who is the author of America-Lite: How Imperial Academia Dismantled Our Culture?", "#1"],
    "Q2": ["Where was #1 educated?", "#2"],
    "Q3": ["Where was Steven Segaloff born?", "#3"],
    "Q4": ["What weekly publication in #3 is issued by #2?", "#4"]
}}
```

Question: In which country is Tuolumne, a city in the county sharing a border with Pinecrest's county in the state where Finding Dory supposedly takes place?
Tips:
```json
{{
    "Q1": ["Pinecrest >> located in the administrative territorial entity", "#1"], 
    "Q2": ["#1 >> shares border with", "#2"], 
    "Q3": ["where is finding dory supposed to take place", "#3"], 
    "Q4": ["Tuolumne, #2 , #3 >> country", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["What county is Pinecrest located in?", "#1"],
    "Q2": ["What county shares a border with #1?", "#2"],
    "Q3": ["Where is Finding Dory supposed to take place?", "#3"],
    "Q4": ["Which country is Tuolumne, #2, #3 located in?", "#4"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE9_4HOP_COMPARISON_SYSTEM_PROMPT = """Your job is to decompose the question into four sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language.", "#1"],
    "Q2": ["A sub-question described in natural language.", "#2"],
    "Q3": ["A sub-question described in natural language.", "#3"],
    "Q4": ["A sub-question described in natural language.", "#4"]
}}
```

Examples:
Question: Who lived longer, Constance Keys or Anthony De Jasay?
Tips:
```json
{{
    "Q1": ["Constance Keys >> date of birth", "#1"],
    "Q2": ["Constance Keys >> date of death", "#2"],
    "Q3": ["Anthony De Jasay >> date of birth", "#3"],
    "Q4": ["Anthony De Jasay >> date of death", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["When was Constance Keys born?", "#1"],
    "Q2": ["When did Constance Keys die?", "#2"],
    "Q3": ["When was Anthony De Jasay born?", "#3"],
    "Q4": ["When did Anthony De Jasay die?", "#4"]
}}
```

Question: Who lived longer, Pannalal Barupal or Thomas Winterflood?
Tips:
```json
{{
    "Q1": ["Pannalal Barupal >> date of birth", "#1"],
    "Q2": ["Pannalal Barupal >> date of death", "#2"],
    "Q3": ["Thomas Winterflood >> date of birth", "#3"],
    "Q4": ["Thomas Winterflood >> date of death", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["When was Pannalal Barupal born?", "#1"],
    "Q2": ["When did Pannalal Barupal die?", "#2"],
    "Q3": ["When was Thomas Winterflood born?", "#3"],
    "Q4": ["When did Thomas Winterflood die?", "#4"]
}}
```

Question: Who lived longer, Sibylle of Cleves or Oona O'Neill?
Tips:
```json
{{
    "Q1": ["Sibylle of Cleves >> date of birth", "#1"],
    "Q2": ["Sibylle of Cleves >> date of death", "#2"],
    "Q3": ["Oona O'Neill >> date of birth", "#3"],
    "Q4": ["Oona O'Neill >> date of death", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["When was Sibylle of Cleves born?", "#1"],
    "Q2": ["When did Sibylle of Cleves die?", "#2"],
    "Q3": ["When was Oona O'Neill born?", "#3"],
    "Q4": ["When did Oona O'Neill die?", "#4"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE10_4HOP_BRIDGE_COMPARISON_SYSTEM_PROMPT = """Your job is to decompose the question into four sub-questions. The sub-questions must be described using natural language, which is complete in one sentence. The sub-questions should start with W/H and be as concise as possible. In addition, some tips will be provided to you, which outline the steps and logic of the decomposition process.
Tips are not entirely natural language, but the output should be natural language.
The output format should satisfy the following:
```json
{{
    "Q1": ["A sub-question described in natural language. You can't start with 'When'.", "#1"],
    "Q2": ["A sub-question described in natural language. You can't start with 'When'.", "#2"],
    "Q3": ["A sub-question described in natural language and the placeholder #1 must be included.", "#3"],
    "Q4": ["A sub-question described in natural language and the placeholder #2 must be included.", "#4"]
}}
```

Examples:
Question: Are director of film Move (1970 Film) and director of film M\u00e9diterran\u00e9e (1963 Film) from the same country?
Tips:
```json
{{
    "Q1": ["Move (1970 film) >> director", "#1"], 
    "Q2": ["M\u00e9diterran\u00e9e (1963 film) >> director", "#2"], 
    "Q3": ["#1 >> country of citizenship", "#3"], 
    "Q4": ["#2 >> country of citizenship", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Who was the director of the film Move (1970 film)?", "#1"],
    "Q2": ["Who was the director of the film M\u00e9diterran\u00e9e (1963 film)?", "#2"],
    "Q3": ["What is the country of citizenship of #1?", "#3"],
    "Q4": ["What is the country of citizenship of #2?", "#4"]
}}
```

Question: Which film has the director born later, A Flame In My Heart or Butcher, Baker, Nightmare Maker?
Tips:
```json
{{
    "Q1": ["A Flame in My Heart >> director", "#1"], 
    "Q2": ["Butcher, Baker, Nightmare Maker >> director", "#2"], 
    "Q3": ["#1 >> date of birth", "#3"], 
    "Q4": ["#2 >> date of birth", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Who was the director of the film A Flame in My Heart?", "#1"],
    "Q2": ["Who was the director of the film Butcher, Baker, Nightmare Maker?", "#2"],
    "Q3": ["When was #1 born?", "#3"],
    "Q4": ["When was #2 born?", "#4"]
}}
```

Question: Do both directors of films Bl\u00fccher (film) and The Good Old Soak have the same nationality?
Tips:
```json
{{
    "Q1": ["The Good Old Soak >> director", "#1"], 
    "Q2": ["Bl\u00fccher (film) >> director", "#2"], 
    "Q3": ["#1 >> country of citizenship", "#3"], 
    "Q4": ["#2 >> country of citizenship", "#4"]
}}
```
Output:
```json
{{
    "Q1": ["Who was the director of the film The Good Old Soak?", "#1"],
    "Q2": ["Who was the director of the film Bl\u00fccher (film)?", "#2"],
    "Q3": ["What is the country of citizenship of #1?", "#3"],
    "Q4": ["What is the country of citizenship of #2?", "#4"]
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

GOLDEN_RELEVANT_SYSTEM_PROMPT = """You are a question answering system. You'll get the question as well as the retrievals. Your job is to determine if the retrievals support answering the question. If the retrievals meet this requirement, respond with the highly relevant retrieval id (only one).
Generate a JSON with a single key "Response" and a value that is a retrieval id. In JSON, put every value as an integer number always, not string.

Examples:
Question: Where was the TV show Gotham filmed?
Retrievals:
    1. Gotham (TV series): In February 2014, it was reported that production would begin in New York City in March. Filming for the first season finished on March 24, 2015.
    2. Triangular trade: A similar triangle to this, called the volta do mar was already being used by the Portuguese, before Christopher Columbus' voyage, to sail to the Canary Islands and the Azores.
Judge:
```json
{{"Response": 1}}
```

Question: What nation provided the most legal immigrants to New York City in Caribbean?
Retrievals:
    1. Dominican Republic: The Dominican Republic is the second - largest Caribbean nation by area (after Cuba) at 48,445 square kilometers (18,705 sq mi), and third by population with approximately 10 million people, of which approximately three million live in the metropolitan area of Santo Domingo, the capital city.
    2. New York City: Ecuador, Colombia, Guyana, Peru, and Brazil were the top source countries from South America for legal immigrants to the New York City region in 2013; the Dominican Republic, Jamaica, Haiti, and Trinidad and Tobago in the Caribbean; Egypt, Ghana, and Nigeria from Africa; and El Salvador, Honduras, and Guatemala in Central America.
Judge:
```json
{{"Response": 2}}
```

Question: What country is Prazeres in?
Retrievals:
    1. Portuguese Empire: Although the royal family returned to Portugal in 1821, the interlude led to a growing desire for independence amongst Brazilians. In 1822, the son of Dom Jo\u00e3o VI, then prince - regent Dom Pedro I, proclaimed the independence of Brazil on September 7, 1822, and was crowned Emperor of the new Empire of Brazil.
    2. Prazeres (Lisbon): Prazeres is a former civil parish (\"freguesia\") in the city and municipality of Lisbon, Portugal. At the administrative reorganization of Lisbon on 8 December 2012 it became part of the parish Estrela.
    3. Brazilian Civil Rights Framework for the Internet: The draft bill was approved by the Brazilian Congress C\u00e2mara dos Deputados on March 25, 2014 and was submitted to the Senado Federal.
Judge:
```json
{{"Response": 2}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

GOLDEN_INFERENCE_SYSTEM_PROMPT = """You are a question answering system. Use the evidence while generating the answers and keep the answers grounded in the evidence. All the evidence theoretically supports the question. If there are multiple answers, generate them all.
Generate a JSON with a single key "Response" and a LIST as value. Each element in the LIST is a short phrase or a few words, and put every element as a string always, not float.

Examples:
Query: In which state is Hertfordshire located?
Evidence:
    1. Hertfordshire: Hertfordshire is the county immediately north of London and is part of the East of England region, a mainly statistical unit. A significant minority of the population across all districts are City of London commuters. To the east is Essex, to the west is Buckinghamshire and to the north are Bedfordshire and Cambridgeshire.
Answer:
```json
{{"Response": ["East of England"]}}
```

Query: When was the North Dakota State Capitol built?
Evidence:
    1. North Dakota State Capitol: The disaster required the construction of a new building during the Great Depression. The tower and wing were built in 1931~1934, at a cost of $2 million. 
Answer:
```json
{{"Response": ["1931~1934"]}}
```

Query: Who plays michael myers in halloween by Rob Zombie?
Evidence:
    1. Tyler Mane: Daryl Karolat (born December 8, 1966) is a Canadian actor and former professional wrestler, better known by the name Tyler Mane. He is known for playing Sabretooth in X-Men and X-Men: The Official Game, Ajax in Troy and Michael Myers in the remake of Halloween and its sequel, Halloween II.
Answer:
```json
{{"Response": ["Daryl Karolat", "Tyler Mane"]}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

GOLDEN_AGGREGATE_SYSTEM_PROMPT = """You are a question answering system. Use the evidence while generating the answer and keep the answer grounded in the evidence. Each piece of evidence is represented as "Question >> Answer", where ">>" means "the Answer to the Question is..."
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Query: Which film came out first, The Love Route or Engal Aasan?
Evidence:
    1. When was The Love Route released? >> February 25, 1915
    2. When was Engal Aasan released? >> July 2009
Answer:
```json
{{"Response": "The Love Route"}}
```

Query: What two skills do Lee Hong-gi and Dee Snider have in common?
Evidence:
    1. What are the skills of Dee Snider? >> singer-songwriter
    2. What are the skills of Lee Hong-gi? >> songwriter
Answer:
```json
{{"Response": "songwriter"}}
```

Query: Do both films The Falcon (Film) and Valentin The Good have the directors from the same country?
Evidence:
    1. Who is the director of The Falcon (Film)? >> Vatroslav Mimica
    2. Who is the director of Valentin The Good? >> Martin Frič
    3. Which country is Vatroslav Mimica from? >> Croatia
    4. Which country is Martin Frič from? >> Czech Republic
Answer:
```json
{{"Response": "No"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

DATE_FORMAT_SYSTEM_PROMPT = """Your task is to convert text dates into numeric dates. Numeric dates is a list with "year", "month", and "day". Missing elements are set to "01".
Generate a JSON with a single key "Response" and a LIST as value. Each element in the LIST is a string, not an integer number.

Examples:
Input: March 29, 1834
Output:
```json
{{"Response": ["1834", "03", "29"]}}
```

Input: 3 March 1836
Output:
```json
{{"Response": ["1836", "03", "03"]}}
```

Input: 1921
Output:
```json
{{"Response": ["1921", "01", "01"]}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

EVALUATE_SYSTEM_PROMPT = """You are a question answering system. Your job is to determine if the predicted answer is correct based on question and golden answers, respond with "Yes" if it is correct, and "No" otherwise. If the predicted answer is more or less informative, you need to carefully check whether it is correct through the question and the golden answer.
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Question: In what year was the termination of the company that worked on USRA Light Pacific?
Golden answer: ["1920"]
Predicted answer: March 1st, 1920
Output:
```json
{{"Response": "Yes"}}
```

Question: When did the Admiral Twin open in the Oil Capitol of the World?
Golden answer: ["1998"]
Predicted answer: 1951
Output:
```json
{{"Response": "No"}}
```

Question: What kind of agency is the the law enforcement bureau that pioneered DNA testing?
Golden answer: ["FBI", "Federal Bureau of Investigation"]
Predicted answer: FBI is primarily a domestic agency
Output:
```json
{{"Response": "Yes"}}
```

Question: The creator of a painting named Hope is noted for creating mosaics in what century?
Golden answer: ["19th", "19th century", "19th-century"]
Predicted answer: 20th century
Output:
```json
{{"Response": "No"}}
```

Question: Where in Plymouth is the base for the operator of Thames class lifeboat?
Golden answer: ["Millbay Docks"]
Predicted answer: Millbay
Output:
```json
{{"Response": "Yes"}}
```

Question: When was the North Dakota State Capitol built?
Golden answers: ["between 1931 and 1934"]
Predicted answer: 1931
Output:
```json
{{"Response": "No"}}
```

Question: What are the roles of Muslims across Islam in India?
Golden answer: ["economics, politics, and culture of India"]
Predicted answer: economics
Output:
```json
{{"Response": "Yes"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

TYPE_SYSTEM_PROMPT = """Given a question, determine what type the question belongs to. Types include:
1. Bridge: A bridge question involves two or more facts that are connected by an intermediate entity (usually an associative link). The bridge question requires finding the intermediary entity, then using it to answer the question.
2. Comparison: A comparison question involves comparing two or more independent facts. The comparison question requires analyzing and comparing the differences or similarities between different facts to draw a conclusion.

Examples:
Question: What language was used by Renana Jhabvala's mother?
Output:
```json
{{"Response": "Bridge"}}
```

Question: Which film came out first, The Love Route or Engal Aasan?
Output:
```json
{{"Response": "Comparison"}}
```

NOTE: Always respond with the JSON object. The question should be preferentially judged as "Bridge" or "Comparison".
Now it's your turn!
"""

BRIDGE_SYSTEM_PROMPT = """Given a bridge question, split it into smaller, independent, and individual subqueries. 
A bridge question involves two or more facts that are connected by an intermediate entity (usually an associative link). The bridge question requires finding the intermediary entity, then using it to answer the question.
For the subquery generation, input a tag "<A>" where the answer of the parent query should come to make the query complete. Specifically,
    1. Subquery is NOT allowed to ask open-ended question. For example, for question "What language was used by Renana Jhabvala's mother?", it is NOT allowed to decompose and ask "Who is Renana Jhabvala?".
    2. Each subquery is a simple fact question, not a question that requires reasoning. For example, "Who lives longer, <A1> or <A2>?" is NOT allowed.

Examples:
Question: What language was used by Renana Jhabvala's mother?
Result:
```json
{{
    "Response": {{
        "Q1": ["Who was Renana Jhabvala's mother?", "<A1>"],
        "Q2": ["What language was used by <A1>?", "<A2>"]
    }}
}}
```

Question: Who is Sobe (Sister Of Saint Anne)'s child-in-law?
Result:
```json
{{
    "Response": {{
        "Q1": ["Who is the child of Sobe (Sister Of Saint Anne)?", "<A1>"],
        "Q2": ["Who is the spouse of <A1>?", "<A2>"]
    }}
}}
```

Question: What followed the last person to live in Versailles in the country that became allies with America after the battle of Saratoga?
Result:
```json
{{
    "Response": {{
        "Q1": ["Who became allies with America after the Battle of Saratoga?", "<A1>"],
        "Q2": ["Who was the last person to live in Versailles?", "<A2>"],
        "Q3": ["What followed <A2> in <A1>?", "<A3>"]
    }}
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

COMPARISON_SYSTEM_PROMPT = """Given a comparison question, split it into smaller, independent, and individual subqueries.
A comparison question involves comparing two or more independent facts. The comparison question requires analyzing and comparing the differences or similarities between different facts to draw a conclusion.
For the subquery generation, input a tag "<A>" where the answer of the parent query should come to make the query complete. Specifically,
    1. Subquery is NOT allowed to ask open-ended question. For example, for question "What language was used by Renana Jhabvala's mother?", it is NOT allowed to decompose and ask "Who is Renana Jhabvala?".
    2. Each subquery is a simple fact question, not a question that requires reasoning. For example, "Who lives longer, <A1> or <A2>?" is NOT allowed.

Examples:
Question: Are Harper High School (Chicago) and Santa Sabina College located in the same country?
Result:
```json
{{
    "Response": {{
        "Q1": ["What country is Santa Sabina College located in?", "<A1>"],
        "Q2": ["What country is Harper High School (Chicago) located in?", "<A2>"]
    }}
}}
```

Question: Who lived longer, Constance Keys or Anthony De Jasay?
Result:
```json
{{
    "Response": {{
        "Q1": ["When was Constance Keys born?", "<A1>"],
        "Q2": ["When did Constance Keys die?", "<A2>"],
        "Q3": ["When was Anthony De Jasay born?", "<A3>"],
        "Q4": ["When did Anthony De Jasay die?", "<A4>"]
    }}
}}
```

Question: Which film has the director born later, A Flame In My Heart or Butcher, Baker, Nightmare Maker?
Result:
```json
{{
    "Response": {{
        "Q1": ["Who was the director of the film A Flame in My Heart?", "<A1>"],
        "Q2": ["Who was the director of the film Butcher, Baker, Nightmare Maker?", "<A2>"],
        "Q3": ["When was <A1> born?", "<A3>"],
        "Q4": ["When was <A2> born?", "<A4>"]
    }}
}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

MHQA_RELEVANT_SYSTEM_PROMPT = """You are a question answering system. You'll get the question as well as the retrievals. Your job is to determine if the retrievals support answering the question. If the retrievals meet this requirement, respond with the highly relevant retrieval id.
Generate a JSON with a single key "Response" and a LIST as value. Each element in the LIST is a retrieval id, and put every element as an integer number always, not string.

Example:
Question: Where was Michael Dulaney born?
Retrievals:
    1. Todd Dulaney: Todd Dulaney Todd Anthony Dulaney (born December 20, 1983) is an American gospel musician, and former baseball player. His music career started in 2011, with the release of the CD version, \"\"Pulling Me Through\"\". This would be his breakthrough released upon the \"\"Billboard\"\" Gospel Albums chart. He would release another album, \"\"A Worshipper's Heart\"\", in 2016 with EntertainmentOne Nashville, 
    2. Dulaney High School: Dulaney High School Dulaney High School is a secondary school in Timonium, Baltimore County, Maryland. The school serves a generally upper-middle class suburban community, with students from Timonium and surrounding areas in Baltimore County. Dulaney is a Blue Ribbon School and ranked #259 nationwide in \"\"Newsweek\"\" magazine's 2010 survey of top public high schools in the U.S.
    3. Dulaney High School: Blue Ribbon School of Excellence in 1995. In 2010, Dulaney was named #259 on \"\"Newsweek\"\" magazine's \"\"1,200 Top U.S. high schools\"\" annual national survey. Dulaney High School Dulaney High School is a secondary school in Timonium, Baltimore County, Maryland. The school serves a generally upper-middle class suburban community,
    4. Todd Dulaney: No. 13 on the Independent Albums chart. Dulaney's wife is Kenyetta Stone-Dulaney, and together they have four children, Tenley, Taylor, Tyler, and Todd Jr., who attend church at Living Word Christian located in Forest Park, Illinois. Todd Dulaney Todd Anthony Dulaney (born December 20, 1983) is an American gospel musician, and former baseball player. His music career started in 2011, with
    5. Clermont (Alexandria, Virginia): Clermont Plantation was built by Benjamin Dulaney in the late 18th century. Dulaney, a friend of George Washington, used the estate as his summer residence. Clermont was large in size with two parlors, eleven bedrooms, and multiple outbuildings. Dulaney's family members were loyalists during the American Revolutionary War and many of them lost their possessions and property.
Judge:
```json
{{"Response": []}}
```

Question: Who wrote the theme song to Charlie Brown?
Retrievals:
    1. A Boy Named Charlie Brown: arranged by John Scott Trotter (who also wrote \"\"I Before E\"\"). The music consisted mostly of uptempo jazz tunes that had been heard since some of the earliest \"\"Peanuts\"\" television specials aired back in 1965; however, for \"\"A Boy Named Charlie Brown\"\", they were given a more \"\"theatrical\"\" treatment, with lusher horn-filled arrangements.
    2. On My Way (Charlie Brown song): which at the end of the video he is seen with his friends who listen to the track and seem to approve then receiving a CD with Brown's label on the front and Brown appearing to go on stage at the end. The following versions of the song are available for sale as digital downloads: The song entered at number seven on the UK Singles Chart on 31 March 2013 \u2015 for the week ending dated 6 April 2013.
    3. A Boy Named Charlie Brown: him to be sent to the principal's office (A few gags from that storyline, however, were also used in \"\"You're in Love, Charlie Brown\"\"). \"\"A Boy Named Charlie Brown\"\" also included several original songs, some of which boasted vocals for the first time: \"\"Failure Face\"\", \"\"I Before E\"\" and \"\"Champion Charlie Brown\"\" (Before this film, musical pieces in Peanuts specials were primarily
    4. Linus and Lucy: ``Linus and Lucy ''is a popular jazz piano composition written by Vince Guaraldi, appearing in many of the Peanuts animated television specials. A Charlie Brown Christmas introduced the song to a television audience of millions of children beginning in 1965. Since that special, the piece has introduced most of the Peanuts TV cartoons, with the exceptions of the specials and other TV programs produced between
    5. Charlie Brown (Coldplay song): own website at 03.00 am on 3 February 2012. On YouTube, the video received over 700,000 views within the first 24 hours of its release. The video was also met with acclaim from critics, who praised its visuals, themes and fast-paced editing. The video features \"\"Shameless\"\" star Elliot Tittensor and \"\"Misfits\"\" star Antonia Thomas. Credits adapted from promotional single liner notes        
Judge:
```json
{{"Response": [4]}}
```

Question: In which state is Hertfordshire located?
Retrievals:
    1. Hertfordshire: Hertfordshire is the county immediately north of London and is part of the East of England region, a mainly statistical unit. A significant minority of the population across all districts are City of London commuters. To the east is Essex, to the west is Buckinghamshire and to the north are Bedfordshire and Cambridgeshire.
    2. Hertfordshire: Hertfordshire is an administrative and historic county situated in the East of England, which is part of the United Kingdom. Within England, Hertfordshire serves as an administrative division and is bordered by Greater London to the south, with its landscape largely encompassed by the London Basin.
    3. Hertfordshire Chain Walk: The Hertfordshire Chain Walk is located in Hertfordshire, England, and consists of 15 linked circular walks. These walks, each of which is between 4.25 and 9 miles, make up a total distance of 87 miles. The tracks pass through villages in East Hertfordshire close to London, the Icknield Way and the Cambridgeshire border.  
    4. University of Hertfordshire: Campus is the university\'s Learning Resource Centre, a combined library and computer centre. The University of Hertfordshire Students\' Union is headquartered at College Lane campus. The College Lane campus is also the location of Hertfordshire International College, which is part of the Navitas group, providing a direct pathway for international students to the University. 
    5. Moor Park, Hertfordshire: Moor Park, Hertfordshire Moor Park is a private residential estate in the Three Rivers District of Hertfordshire, England. Located approximately northwest of central London and adjacent to the Greater London boundary, it is a suburban residential development. It takes its name from Moor Park, a country house which was originally built in 1678\u20139 for James,
Judge:
```json
{{"Response": [1, 2]}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

MHQA_REWRITE_SYSTEM_PROMPT = """You are a question answering system. Given a question, create an answer to the question.
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Example:
Question: In which state is Hertfordshire located?
Answer:
```json
{{"Response": "East of England"}}
```

Question: When was PolyGram Filmed Entertainment abolished?
Answer:
```json
{{"Response": "1999"}}
```

Question: Who plays michael myers in halloween by Rob Zombie?
Answer:
```json
{{"Response": "Daryl Karolat"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

MHQA_AGGREGATE_SYSTEM_PROMPT = """You are a question answering system. Use the evidence while generating the answer and keep the answer grounded in the evidence. Each piece of evidence is represented as "Question >> Answer", where ">>" means "the Answer to the Question is...".
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Question: When was the baseball team winning the world series in 2015 baseball created?
Evidence:
    1. Who won the world series in 2015 baseball? >> Kansas City Royals
    2. When was Kansas City Royals created? >> 1969
Answer:
```json
{{"Response": "1969"}}
```

Question: What two skills do Lee Hong-gi and Dee Snider have in common?
Evidence:
    1. What are the skills of Dee Snider? >> singer-songwriter
    2. What are the skills of Lee Hong-gi? >> songwriter
Answer:
```json
{{"Response": "songwriter"}}
```

Question: Which film came out first, The Love Route or Engal Aasan?
Evidence:
    1. When was The Love Route released? >> February 25, 1915
    2. When was Engal Aasan released? >> July 2009
Answer:
```json
{{"Response": "The Love Route"}}
```

Question: Do both films The Falcon (Film) and Valentin The Good have the directors from the same country?
Evidence:
    1. Who is the director of The Falcon (Film)? >> Vatroslav Mimica
    2. Who is the director of Valentin The Good? >> Martin Frič
    3. Which country is Vatroslav Mimica from? >> Croatia
    4. Which country is Martin Frič from? >> Czech Republic
Answer:
```json
{{"Response": "No"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

VANILLA_QA_SYSTEM_PROMPT = """You are a question answering system. Given a question, create an answer to the question.
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Example:
Question: In which state is Hertfordshire located?
Answer:
```json
{{"Response": "East of England"}}
```

Question: When was PolyGram Filmed Entertainment abolished?
Answer:
```json
{{"Response": "1999"}}
```

Question: Who plays michael myers in halloween by Rob Zombie?
Answer:
```json
{{"Response": "Tyler Mane"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

RAG_QA_SYSTEM_PROMPT = """You are a question answering system. Use the retrievals while generating the answers and keep the answers grounded in the retrievals.
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Query: In which state is Hertfordshire located?
Retrievals:
    1. Hertfordshire: Hertfordshire is the county immediately north of London and is part of the East of England region, a mainly statistical unit. A significant minority of the population across all districts are City of London commuters. To the east is Essex, to the west is Buckinghamshire and to the north are Bedfordshire and Cambridgeshire.
    2. Hertfordshire: Hertfordshire is an administrative and historic county situated in the East of England, which is part of the United Kingdom. Within England, Hertfordshire serves as an administrative division and is bordered by Greater London to the south, with its landscape largely encompassed by the London Basin.
    3. Hertfordshire Chain Walk: The Hertfordshire Chain Walk is located in Hertfordshire, England, and consists of 15 linked circular walks. These walks, each of which is between 4.25 and 9 miles, make up a total distance of 87 miles. The tracks pass through villages in East Hertfordshire close to London, the Icknield Way and the Cambridgeshire border.  
    4. University of Hertfordshire: Campus is the university\'s Learning Resource Centre, a combined library and computer centre. The University of Hertfordshire Students\' Union is headquartered at College Lane campus. The College Lane campus is also the location of Hertfordshire International College, which is part of the Navitas group, providing a direct pathway for international students to the University. 
    5. Moor Park, Hertfordshire: Moor Park, Hertfordshire Moor Park is a private residential estate in the Three Rivers District of Hertfordshire, England. Located approximately northwest of central London and adjacent to the Greater London boundary, it is a suburban residential development. It takes its name from Moor Park, a country house which was originally built in 1678\u20139 for James,
Answer:
```json
{{"Response": "East of England"}}
```

Query: Who plays michael myers in halloween by Rob Zombie?
Retrievals:
    1. Halloween (2007 film): Halloween is a 2007 American slasher film written, directed, and produced by Rob Zombie. The film stars Tyler Mane as the adult Michael Myers, Malcolm McDowell as Dr. Sam Loomis. Rob Zombie\'s ""reimagining"" follows the premise of John Carpenter\'s original, with Michael Myers stalking Laurie Strode and her friends on Halloween night.
    2. Halloween (1978 film): A remake was released in 2007, directed by Rob Zombie, which itself was followed by a 2009 sequel. An eleventh installment was released in the United States in 2018. The film, directed by David Gordon Green, is a direct sequel to the original film while disregarding the previous sequels from canon, and retconing the ending of the first film. A sequel is in early development.
    3. Rob Zombie: Rob Zombie Rob Zombie (born Robert Bartleh Cummings; January 12, 1965) is an American musician and filmmaker who rose to fame as a founding member of the heavy metal band White Zombie, releasing four studio albums with the band. He is the older brother of Spider One, lead vocalist for American rock band Powerman 5000. Zombie's first solo effort was a song titled \"\"Hands of Death (Burn Baby Burn)\"\" (1996)
    4. Halloween II (2009 film): by The Weinstein Company, and planned to be released in 2012. That film was ultimately cancelled in 2012. \"\"Halloween 3D\"\" was planned to have Michael Myers stalk Laurie Strode while she was confined in a mental asylum. Halloween II (2009 film) Halloween II is a 2009 American slasher film written, directed, and produced by Rob Zombie. 
    5. Laurie Strode: Laurie Strode Laurie Strode is a fictional character in the \"\"Halloween\"\" franchise, portrayed by actresses Jamie Lee Curtis and Scout Taylor-Compton. One of the two main protagonists of the overall series (the other being Dr. Sam Loomis), she appears in seven of the eleven \"\"Halloween\"\" films, first appearing in John Carpenter's original 1978 film. 
Answer:
```json
{{"Response": "Tyler Mane"}}
```

Query: Who wrote the theme song to Charlie Brown?
Retrievals:
    1. Todd Dulaney: Todd Dulaney Todd Anthony Dulaney (born December 20, 1983) is an American gospel musician, and former baseball player. His music career started in 2011, with the release of the CD version, \"\"Pulling Me Through\"\". This would be his breakthrough released upon the \"\"Billboard\"\" Gospel Albums chart. He would release another album, \"\"A Worshipper's Heart\"\", in 2016 with EntertainmentOne Nashville, 
    2. Dulaney High School: Dulaney High School Dulaney High School is a secondary school in Timonium, Baltimore County, Maryland. The school serves a generally upper-middle class suburban community, with students from Timonium and surrounding areas in Baltimore County. Dulaney is a Blue Ribbon School and ranked #259 nationwide in \"\"Newsweek\"\" magazine's 2010 survey of top public high schools in the U.S.
    3. Dulaney High School: Blue Ribbon School of Excellence in 1995. In 2010, Dulaney was named #259 on \"\"Newsweek\"\" magazine's \"\"1,200 Top U.S. high schools\"\" annual national survey. Dulaney High School Dulaney High School is a secondary school in Timonium, Baltimore County, Maryland. The school serves a generally upper-middle class suburban community,
    4. Todd Dulaney: No. 13 on the Independent Albums chart. Dulaney's wife is Kenyetta Stone-Dulaney, and together they have four children, Tenley, Taylor, Tyler, and Todd Jr., who attend church at Living Word Christian located in Forest Park, Illinois. Todd Dulaney Todd Anthony Dulaney (born December 20, 1983) is an American gospel musician, and former baseball player. His music career started in 2011, with
    5. Clermont (Alexandria, Virginia): Clermont Plantation was built by Benjamin Dulaney in the late 18th century. Dulaney, a friend of George Washington, used the estate as his summer residence. Clermont was large in size with two parlors, eleven bedrooms, and multiple outbuildings. Dulaney's family members were loyalists during the American Revolutionary War and many of them lost their possessions and property.
Answer:
```json
{{"Response": "Vince Guaraldi"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

RAG_MHQA_SYSTEM_PROMPT = """You are a question answering system. Use the retrievals while generating the answers and keep the answers grounded in the retrievals.
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Query: Where did the Baldevins bryllup director born?
Retrievals:
    1. Baldevins bryllup: Baldevins bryllup () is a 1926 Norwegian comedy film directed by George Schn\u00e9evoigt, starring Einar Sissener and Victor Bernau. The film is based on a play by Vilhelm Krag, and tells the story of how Simen S\u00f8rensen (Bernau) manages to get his friend Baldevin Jonassen (Sissener) married to the lady next door. The film was renovated in 2006, for the 100-years anniversary of Kristiansand Cinema.
    2. Anne Marit Jacobsen: Anne Marit Jacobsen Anne Marit Jacobsen (born 7 November 1946) is a Norwegian stage and film actress. She was born in Oslo as the daughter of sculptor Thorbj\u00f8rn Sigurd Jacobsen and opera singer Randi Heide Steen. She has been assigned to the National Theatre in Oslo from 1970, and has also participated in revue, television and film. Among her films roles are the title
    3. Eilif Armand: Eilif Armand Eilif Armand (18 March 1921 \u2013 28 November 1993) was a Norwegian actor. He was born in Bergen to businessman Sverre Andreassen and Maggi S\u00f8rensen, and was the father of actresses Fr\u00f8ydis Armand, Gisken Armand and Merete Armand. He made his stage debut at Den Nationale Scene in 1946, as \"\"Jesus\"\" in Nordahl Grieg's play \"\"Barabbas\"\".
    4. George Schn\u00e9evoigt: Schn\u00e9evoigt was born in Copenhagen, Denmark to actress Siri Schn\u00e9evoigt, and he is the father of actor and director Alf Schn\u00e9evoigt.
    5. Bill.mrk: Bryllup: Bill.mrk: Bryllup Bill.mrk: Bryllup was a Norwegian reality TV series broadcast on TV3 in 2004. The program was produced by Strix Televisjon AS. One woman was going to meet as many men as she could during the course of 45 days. Each man got at least 24 hours with her, then she could ask the next man to come in. At the same time she was going to prepare her own wedding,
Answer:
```json
{{"Response": "Copenhagen"}}
```

Query: Who lived longer, Billy Todd or Salvador Videgain?
Retrievals:
    1. Salvador Videgain: Salvador Videgain Garc\u00eda( Madrid, February 26, 1886, \u2013 Madrid, October 12, 1947) was a famous actor of comedy and zarzuela during the first half of the 20th century in Spain and Am\u00e9rica. He was born and died in Madrid. He was known artistically as Salvador Videgain, was a theatrical entrepreneur, author, actor, theater director, Spanish.
    2. Salvador Videgain Go\u0301mez: Salvador Videgain G\u00f3mez Salvador Videgain G\u00f3mez (1845\u20131906) was a Spanish actor, singer, producer and composer. Videgain was born in M\u00e1laga in 1845. He is of Spanish, English, Irish and Basque ancestry. Videgain married actress Antonia Garc\u00eda de Videgain in 1868 and founded the family artistic Videgain the most lounger in the history of theatre in Europe.
    3. Salvador Videgain Go\u0301mez: awards and nominations for his work in theatre. He sang with famous voices such as Jos\u00e9 Sigler, Enrique Lacasa, Bonifacio Pinedo, Ventura de la Vega and Miguel Fleta. He is one of the few singers best known as an actor to be recognized in the 19th century. Salvador Videgain G\u00f3mez Salvador Videgain G\u00f3mez (1845\u20131906) was a Spanish actor, singer, producer and composer.
    4. Juan Jose\u0301 Videgain: various workshop programs and popular film festival, in Spain has provided much-needed support for independent filmmakers as Rub\u00e9n Jim\u00e9nez or Jack Newman. Juan Jos\u00e9 Videgain Juan Jos\u00e9 Videgain (born 30 July 1975) is a Spanish writer, actor and director. Most of Videgain's books have reached cult status thanks to their weird sense of humor in Spain.
    5. Billy Todd: Billy Todd (September 26, 1929 \u2013 November 30, 2008) was the bass singer for the Florida Boys Quartet in the Southern Gospel music industry from the 1950s to 1972. 
Answer:
```json
{{"Response": "Billy Todd"}}
```

Query: Which film has the director born later, A Flame In My Heart or Butcher, Baker, Nightmare Maker?
Retrievals:
    1. A Flame in My Heart: A Flame in My Heart is a 1987 French- Swiss drama film directed by Alain Tanner.
    2. Night Warning: Night Warning Night Warning (also known as Butcher, Baker, Nightmare Maker) is a 1982 American exploitation horror film directed by William Asher, and starring Susan Tyrrell, Jimmy McNichol, Julia Duffy, and Bo Svenson. Framed as a contemporary Oedipus tale, the plot focuses on a teenager who, raised by his neurotic aunt, finds himself at the center of a murder investigation after she stabs a man to death in their house.
    3. Alain Tanner: anner is best known for his movies \"\"Jonas qui aura 25 ans en l'an 2000\"\" (\"\"Jonah Who Will Be 25 in the Year 2000\"\"), \"\"Dans la ville blanche\"\" (\"\"In the White City\"\") and \"\"Messidor\"\". \"\"Dans la ville blanche\"\" was entered into the 33rd Berlin International Film Festival. Alain Tanner Alain Tanner (born 6 December 1929) is a Swiss film director. Tanner studied
    4. William Asher: William Asher William Milton Asher (August 8, 1921 \u2013 July 16, 2012) was an American television and film producer, film director, and screenwriter. He was one of the most prolific early television directors, producing or directing over two dozen series. With television in its infancy, Asher introduced the sitcom
    5. My Heart Is Calling You: My Heart Is Calling You My Heart Is Calling You (French: Mon coeur t'appelle) is a 1934 French-German musical film directed by Carmine Gallone and Serge V\u00e9ber, written by Ernst Marischka, produced by Arnold Pressburger. The film stars Jan Kiepura, Danielle Darrieux and Lucien Baroux. The music score is by Robert Stolz. Its English (\"\"My Heart is Calling\"\") and
Answer:
```json
{{"Response": "A Flame In My Heart"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

BRIDGE_AGGREGATE_SYSTEM_PROMPT = """You are a question answering system. Use the evidence while generating the answer and keep the answer grounded in the evidence. Each piece of evidence is represented as "Question >> Answer", where ">>" means "the Answer to the Question is...".
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Question: When was the baseball team winning the world series in 2015 baseball created?
Evidence:
    1. Who won the world series in 2015 baseball? >> Kansas City Royals
    2. When was Kansas City Royals created? >> 1969
Answer:
```json
{{"Response": "1969"}}
```

Question: When did the French come to the region where Philipsburg is located?
Evidence:
    1. Where is Philipsburg located? >> Sint Maarten
    2. What terrain feature is located in the Sint Maarten region? >> Great Bay and Great Salt Pond
    3. When did the French come to Great Bay and Great Salt Pond? >> 1625
Answer:
```json
{{"Response": "1625"}}
```

Question: How many people who started the great migration of the Slavs live in the country the football tournament is held?
Evidence:
    1. Who started the Great Migration of the Slavs? >> Germans
    2. Where was the football tournament held? >> Brazil
    3. How many of Germans live in Brazil? >> 5 million
Answer:
```json
{{"Response": "5 million"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

COMPARISON_AGGREGATE_SYSTEM_PROMPT = """You are a question answering system. Use the evidence while generating the answer and keep the answer grounded in the evidence. Each piece of evidence is represented as "Question >> Answer", where ">>" means "the Answer to the Question is...".
Generate a JSON with a single key "Response" and a value that is a short phrase or a few words. In JSON, put every value as a string always, not float.

Examples:
Question: Which film came out first, The Love Route or Engal Aasan?
Evidence:
    1. When was The Love Route released? >> February 25, 1915
    2. When was Engal Aasan released? >> July 2009
Answer:
```json
{{"Response": "The Love Route"}}
```

Question: Who lived longer, Dina Vierny or Muhammed Bin Saud Al Saud?
Evidence:
    1. When was Dina Vierny born? >> 25 January 1919
    2. When did Dina Vierny die? >> 20 January 2009
    3. When was Muhammed Bin Saud Al Saud born? >> 21 March 1934
    4. When did Muhammed Bin Saud Al Saud die? >> 8 July 2012
Answer:
```json
{{"Response": "Dina Vierny"}}
```

Question: Do both films The Falcon (Film) and Valentin The Good have the directors from the same country?
Evidence:
    1. Who is the director of The Falcon (Film)? >> Vatroslav Mimica
    2. Who is the director of Valentin The Good? >> Martin Frič
    3. Which country is Vatroslav Mimica from? >> Croatia
    4. Which country is Martin Frič from? >> Czech Republic
Answer:
```json
{{"Response": "No"}}
```

NOTE: Always respond with the JSON object.
Now it's your turn!
"""

HYDE_SYSTEM_PROMPT = """Please write a passage to answer the question."""

