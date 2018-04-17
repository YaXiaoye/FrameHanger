# FrameHanger

A tool to extract static and dynamic injected iframes

# Install dependencies

```
bash install.sh
```

## How to use



## A Demo

The demo shows that FrameHange could extract injected iframes from obfuscated JavaScript code.
The JavaScript code is located at benchmark/dynamic_obfuscation.html.

python dynamic_detection.py benchmark/dynamic_obfuscation.html .


![](https://github.com/ririhedou/FrameHanger/blob/master/benchmark/demo.gif)

## Disclaim

A research prototype, use at your own risk

If you feel this tool is helpful, citing the paper is highly encouraged.

```
@inproceedings{framehanger,
  title={FrameHanger: Evaluating and Classifying Iframe Injection at Large Scale},
  author={Ke Tian, Zhou Li, Kevin Bowers and Danfeng Yao},
  booktitle={Proc. of 14th EAI International Conference on Security and Privacy in Communication Networks (SecureComm)},
  year={2018}
}
```