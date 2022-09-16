import requests


'''
２次元配列から値を取り出して、１次元配列に入れたものを返す

param multi_array: ２次元配列
param row: ２次元配列の列のindex
param column: ２次元配列の行のindex
param final_array: ２次元配列から取り出して来た値を入れる１次元配列
'''
def unpack_multi_array(multi_array: list, row: int, column: int, final_array: list[str]) -> list[str]:
    if row > len(multi_array) - 1:
        return final_array
    if column > len(multi_array[row]) - 1:
        return unpack_multi_array(multi_array, row + 1, 0, final_array)
    final_array_copy: list[str] = final_array.copy()
    final_array_copy.append(multi_array[row][column])
    return unpack_multi_array(multi_array, row, column + 1, final_array_copy)

'''
指定したファイルの内容を取り出して、配列に格納し、それを返す

param file_path: ファイルのパス
param split_char: ファイルの文章の区切り文字
'''
def read_lines(file_path: str, split_char: str) -> list[str]:
    with open(file_path, "r") as file:
        # index.html,style.css みたいなファイルの内容になっているから、splitで一つ一つ取り出してる
        lines: list = [line.split(split_char) for line in file.readlines()]
        return list(map(
            lambda word: word.replace("\n", ""),
            unpack_multi_array(lines, 0, 0, [])
        ))

'''
指定したurlの隠れたディレクトリーを総当たりで調べて、見つけたディレクトリーに行ける
urlを配列にして返す

param url: ディレクトリーを見つけたいurl
param wordlist_path: 総当たりに使うディレクトリー名が記述されたテキストファイルのパス
'''
def find_hidden_directories(url: str, wordlist_path: str) -> list[str]:
    words: list[str] = read_lines(wordlist_path, ",")
    predicted_urls: list[str] = [url + word for word in words]
    return list(filter(
        lambda predicted_url: requests.get(predicted_url).status_code == 200,
        predicted_urls
    ))

if __name__ == "__main__":
    print(find_hidden_directories("https://www.google.com/", "resource/wordlist.txt"))
