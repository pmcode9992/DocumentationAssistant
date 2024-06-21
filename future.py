import concurrent.futures

from filestr import genSummary

list_ofpaths = ["/Users/rejonasusan/Desktop/jobe/asset.css",
                "/Users/rejonasusan/Desktop/jobe/hello.html"]

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futurestuff = {executor.submit(genSummary,pth) : pth for pth in list_ofpaths}
    for future in concurrent.futures.as_completed(futurestuff):
        summary = futurestuff[future]
        try:
            print(future.result())
        except Exception as exc:
            print(exc)

