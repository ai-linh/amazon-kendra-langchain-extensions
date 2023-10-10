#!/bin/bash

INFILE=$1

perl -p -e's/The customer (can|may|should|must)/You $1/g' $INFILE

#perl -p -e's/^Answer: (.*) AI language model(.*)$/Answer: REPLACE_WITH_I_DONT_KNOW_ANSWER/g'
#perl -p -e's/^(.*) AI language model(.*)$/REPLACE_WITH_I_DONT_KNOW_ANSWER/g'

# responses_20230809_2_3.txt
perl -p -e's/but as an AI language model, //g' # 5
perl -p -e's/As an AI language model, //gi' # 180
perl -p -e's/I am an AI language model and /I/g' # 2

based on the information provided in the knowledge base
based on the available information

# responses_20230809_2_5.txt
sed '/^Traceback/,/^----/{/^Traceback/!{/^----/!d;};}'
perl -p -i -e's/Traceback \(most recent call last\):/Answer: I'\''m sorry I can'\''t provide an answer at the moment, please check the Telstra website./g'

# responses_20230809_2_6.txt
sed '/Note:/d'
sed '/Note that/d'
perl -p -e's/(If|However|Alternatively)(.*) you can contact Telstra customer support for further assistance.//g'
perl -p -i -e's/They will be able to assist you(.*)\.//g'
perl -p -i -e's/you can take the following steps:/please:/g'
perl -p -i -e's/you need to follow these steps:/please:/g'
perl -p -i -e's/you can follow these steps:/please:/g'

# responses_20230809_2_7.txt
perl -p -e's/It is important to note(.*)\.//g'
perl -p -i -e's/However, based on the knowledge base provided,/However,/g'
perl -p -i -e's/However, based on the information provided,/However,/g'
perl -p -i -e's/I cannot provide specific instructions on how to contact Telstra customer support\. However, you can/You can/g'
perl -p -i -e's/here are some general troubleshooting steps you can take/please try these steps/g'
perl -p -i -e's/Please refer to the knowledge base/Please check the Telstra website/g'
perl -p -i -e's/ as it is not included in the knowledge base//g'
perl -p -i -e's/Please refer to the document(.*)\./I can send you a link with more information:/g'
perl -p -i -e's/Please provide me with your bank account details or credit\/debit card details so that I can set it up for you\./Please contact Telstra customer support on 132200\./g'
perl -p -i -e's/Alternatively, you can contact Telstra(.*)\.//g'
perl -p -i -e's/Please (call|contact) us on 13 22 00 and say "(.*)"/Please contact us on 132200/g'
perl -p -i -e's/Please let me know if you would like me to assist you with this.//g'
perl -p -i -e's/If you need further assistance, you can contact Telstra customer service.//g'
perl -p -i -e's/or by contacting Telstra directly/or calling 132200/g'
perl -p -i -e's/or contacting Telstra customer support./or calling 132200./g'

# using Jurassic2-Ultra

Rewrite the description below on a few lines and reduce repetition

Description:
To port your mobile service to Telstra, you will need to provide the following information:

1. Your full name, address, and date of birth.
2. Your current mobile phone number and account number.
3. Your new mobile phone number and account number.
4. Your current mobile phone provider's name and account number.
5. Your new mobile phone provider's name and account number.
6. Your current mobile phone's IMEI number.
7. Your new mobile phone's IMEI number.
8. Your current mobile phone's SIM card number.
9. Your new mobile phone's SIM card number.
10. Your current mobile phone's PIN code.
11. Your new mobile phone's PIN code.
12. Your current mobile phone's security code.
13. Your new mobile phone's security code.
14. Your current mobile phone's account balance.
15. Your new mobile phone's account balance.
16. Your current mobile phone's billing address.
17. Your new mobile phone's billing address.
18. Your current mobile phone's payment method.
19. Your new mobile phone's payment method.
20. Your current mobile phone's contract end date.
21. Your new mobile phone's contract start date.
22. Your current mobile phone's handset type.
23. Your new mobile phone's handset type.
24. Your current mobile phone's service provider.
25. Your new mobile phone's service provider.
26. Your current mobile phone's account status.
27. Your new mobile phone's account status.
28. Your current mobile phone's account type.
29. Your new mobile phone's account type.
30. Your current mobile phone's account balance.
31. Your new mobile phone's account balance.
32. Your current mobile phone's billing address.
33. Your new mobile phone's billing address.
34. Your current mobile phone's payment method.
35. Your new mobile phone's payment method.
36. Your current mobile phone's contract end date.
37. Your new mobile phone's contract start date.
38. Your current mobile phone's handset type.
39. Your new mobile phone
##

Answer:
