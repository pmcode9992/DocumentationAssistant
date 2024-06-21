import concurrent.futures

from filestr import genSummary

list_ofpaths = ["/Users/pranav/DemoProject/Script/commission.java",
                "/Users/pranav/DemoProject/Script/Da1q1.java",
                "/Users/pranav/DemoProject/Script/Da1q2.java",
                "/Users/pranav/DemoProject/Script/Da1q3.java"]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futurestuff = {executor.submit(genSummary,pth) : pth for pth in list_ofpaths}
    for future in concurrent.futures.as_completed(futurestuff):
        summary = futurestuff[future]
        try:
            data = future.result()
        except Exception as exc:
            print(exc)
        print(data)

