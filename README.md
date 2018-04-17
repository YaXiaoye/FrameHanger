# Welcome to FrameHanger
```
  ______                        _    _
 |  ____|                      | |  | |
 | |__ _ __ __ _ _ __ ___   ___| |__| | __ _ _ __   __ _  ___ _ __
 |  __| '__/ _` | '_ ` _ \ / _ \  __  |/ _` | '_ \ / _` |/ _ \ '__|
 | |  | | | (_| | | | | | |  __/ |  | | (_| | | | | (_| |  __/ |
 |_|  |_|  \__,_|_| |_| |_|\___|_|  |_|\__,_|_| |_|\__, |\___|_|
                                                    __/ |
                                                   |___/
```

FrameHanger is a tool to extract statically and dynamically injected iframes from webpages

It is able to

- [x] Extract statically injected Iframe
- [x] Gather information on the Iframe and its host HTML content
- [x] Selectively and Dynamically executing JavasScript to detect dynamic Iframe injection
- [x] Detect iframe destinations within JavaScript


## Install dependencies

```
bash install.sh
```

## How to use
```
python main.py -h
usage: main.py [-h] [-s] [-d] [-o OUTPUTDIR] -f HTMLFILE

Iframe injection detection

optional arguments:
  -h, --help            show this help message and exit
  -s, --static          Static analyser for Tag-based iframe injection
  -d, --dynamic         Dynamic analyser for JS-based iframe injection
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Output directory, default is the current directory
  -f HTMLFILE, --htmlfile HTMLFILE
                        the HTML File needs to be analyzed

```

## Demo

The demo shows that FrameHange could extract injected iframes from HTML webapges and obfuscated JavaScript code.
The JavaScript code is located at benchmark/dynamic_obfuscation.html.

```
python main.py -f benchmark/dynamic_obfuscation.html --dynamic
#the JS code is highly obfuscated by attackers

python main.py -f benchmark/static_iframe.html --static
```

![](https://github.com/ririhedou/FrameHanger/blob/master/benchmark/demo.gif)


## Extra

We also provide scripts to enable running the scripts with xvfb on a server with multiple processes.

Please check xvfb-run-safe.sh and run_paralled_linux.sh

## FAQ

- Selenium exception: it is due to the chromedriver version. Check this closed issue [ISSUE](https://github.com/ririhedou/FrameHanger/issues/2)
- Feature extraction: we did not provide the features due to intellectual property restrictions.

## Disclaimer

A research prototype, use at your own risk under the License. Thanks

If you feel this tool is helpful, citing the paper is highly encouraged.

```
@inproceedings{framehanger,
  title={FrameHanger: Evaluating and Classifying Iframe Injection at Large Scale},
  booktitle={Proc. of 14th EAI International Conference on Security and Privacy in Communication Networks (SecureComm)},
  year={2018}
}
```

## Acknowledgement

Thanks @Tigerly and @xiaodong-yu for reproduction testing.

Current version is 0.0.1