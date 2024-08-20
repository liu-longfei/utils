en_srt = r"D:\data\GoogleDownload\Let_is_build_the_GPT_Tokenizer.srt"
zh_srt = r"D:\data\GoogleDownload\Let_is_build_the_GPT_Tokenizer-zh.srt"
merge_srt = r"D:\data\GoogleDownload\Let_is_build_the_GPT_Tokenizer-merge.srt"

with open(en_srt, 'r', encoding='utf-8') as f:
    en_list = f.readlines()
print(len(en_list))

with open(zh_srt, 'r', encoding='utf-8') as f:
    zh_list = f.readlines()
print(len(zh_list))

with open(merge_srt, 'w', encoding='utf-8') as f:
    for i in range(0, len(en_list), 4):
        if en_list[i].strip() == zh_list[i].strip() and en_list[i+1].strip() == zh_list[i+1].strip():
            f.write(en_list[i].strip()+'\n')
            f.write(en_list[i+1].strip()+'\n')
            f.write(en_list[i+2].strip()+'\n')
            f.write(zh_list[i+2].strip()+'\n')
        else:
            print(en_list[i].strip(), zh_list[i].strip(), en_list[i+1].strip(), zh_list[i+1].strip())
        f.write('\n')
