

This is project is forked directly from Tao0Lu/Arknights-Cheater and GhostStar/Arknights-Armada. This folder contains all files that you need to hack ArkNights (curr ver) but your account is highly likely to be banned.


Tested under win10 + powershell.



1. Run the following command in the powershell of your PC:
    ```
    .\mitmweb.exe
    ```

    Your default web-broser should promp a status page after running the command. The powershell will also tell you:
    ```
    Proxy server listening at http://*:8080
    ```
    meaning that the `port` is 8080. (your port number might be different)

2. Check the IPv4 address of your PC.

3. Make sure your device (phone or simulator) is connected to the same network as your PC.

4. Set up your device's Internet Proxy. (Details: https://github.com/Tao0Lu/Arknights-Cheater) Port number used in the link is 12450, change it to 8080 (or whatever you get from step 1.)



5. Login to the game. Your squads (squad-1 to squad-4) should not contain any operator that does not have any skill (i.e. 1-star or 2-star operators are not allowed)

6. Turn off everything. (powershell, arknights-app).

7. Modify myproxy.py.

7. run command in PC:
    ```
    .\mitmweb.exe -s myproxy.py
    ```

8. If nothing wrong, you are ready to go.