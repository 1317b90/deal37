from alipay import AliPay
from alipay.utils import AliPayConfig

USERNAME='root'
PASSWORD='Fu0xuan.112'
HOSTNAME='47.109.71.57'
PORT='3306'
DATABASE='deal37'
CHARSET='utf8mb4'
SQL_URL=('mysql://'+
        USERNAME+':'+PASSWORD+'@'+
        HOSTNAME+':'+PORT+'/'+
        DATABASE)

# 支付宝支付相关配置
def create_alipay():
    app_private_key_string = "-----BEGIN RSA PRIVATE KEY-----\n" + \
        "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCFS18LFqnVfs/i" + \
        "4Uc2zk/L20aB3woUWhlk27pd6bXaWP6z8owiWlcWWTPkuzj1BMVJH1I0fQ8y5107" + \
        "O8IjWE/x7n3JQ/3pkr9b095HLrJGZIZWamM/OC7sJN8RtJ2ojirGMU9nV9YMFNej" + \
        "oidWlt7sEFA2xpLQEzMibDFTza3EBvZB6vKspBfj7fWq5zbk8f0ETsPN4qaWxMMb" + \
        "OF6Xi6dnLVraoknYMepwdqUs6+FG6EBLLUbZFFCxEVkQlrx7AtmYBeHpV0H6GvVD" + \
        "alByUTqd/0cmpPAfxv/7pdMgSCrXQ3mzd8fxF+G+Oz52AdQABIb/s08PQnPrcCm8" + \
        "lc9DAb4FAgMBAAECggEBAIHvOAXqIMISLPoAGlhtgtG4vaFp1zyBm9F6c9CKOxBO" + \
        "wnKNlFcEc3JAoFpuuxX1gY9HLe4mnoNDj9lm5ldoBf5TOmDQm5ptx4XvIPWIqpX9" + \
        "9goVCQwea3ccdiqfQzSE6WNru/iEYg5C3vYO4oQA6+t394l9xq14mdcLWoZTr/iu" + \
        "XIQvOucw3jg2TtHOz+M6n96rbJtPv/+QRUnFrb/V8AbGVjo4+Pyv4wn7px0gac7g" + \
        "FZxZNtRzliRVdtLagfPoV6fWgGClOyllA6O179clV62Oqilha5A0egxAaDvLh2Kn" + \
        "LOopUmkqjDss1EF3Z2nYBXuxKKeqcG9M2pL49zUwAGECgYEAupSutv+QCdqGHaUy" + \
        "X/NZmMSkkXjeAGRPwnfAbiF4rthtKVo9BD8O425oFpMdS5r3yvklmSfeKTIVwURS" + \
        "FwQ7b5c41DWiR26A2EQj6HEG+fnMga8v5gVNAsAtQ3xk9Lf+0qG33/bQmSIfXTgL" + \
        "YnU+R1tdMQxqQkhHSX/X/p+bZUkCgYEAtuNOMnEafiVXe3i15Q2MJjIt7qXFE+al" + \
        "0qPE6VmzS6oCofs+WFda6bMsHyxohYJqx7b54IE/aJXWYafF85Md4Avoh7BHQiCg" + \
        "BQ4kuDNoSYSLSJUBAt4wIq5BYEEVPJCjPH4TSSNmh7pzgOpwHViGwNG3Ilj8pqga" + \
        "eHWhKKXW3t0CgYBTR3IEdGWSQFuEd+vYMAJZ0cuyssREYIHJRzI49e+r+yYeQwzh" + \
        "DFRU5z7GdLuqt2zKyBIkHktnD9ft/9S0OUteL51J+vaH86bG4QM2CN0YTosdh1hV" + \
        "zx/kjmqlqKxXHpk64rvz13KcJ0LglNdgBvzZVMpvzh7PnvtSryF1oT/3IQKBgQCp" + \
        "NVdVDhYf3ja5cy5/lPA1Kroakd7sEbscTw9Rgv+DIvG6onTFUVU44eARm4m89LQM" + \
        "wXshPxPGlNM7mPlp6ZR7hSkH2Y2kXgEPjE1m65Eya+JeLhY4bBAHFkhAYRbf6UZO" + \
        "Iqt/QLSNIXHaNY2zaQOMBLw2mDRxkRikmNiZfg52NQKBgEME4nOI625aes+NNIdH" + \
        "Jr0twCPgxNl0E9aee+RUExo8tTyuyiA8X59Op03UbqU8XaymBvqzyCzJG6HjK/lK" + \
        "/EOsH2YLQXonEtnD3n/33VEL6CTlH6NHN/d96REnpokydLnffxuuTc/Iwuw/Lcw4" + \
        "qYfI3a5JnGF3q2uapN8nSe8c" + \
        "\n-----END RSA PRIVATE KEY-----"

    alipay_public_key_string = "-----BEGIN PUBLIC KEY-----\n" + \
        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs5hVkSYbgEFCpU7DK776" + \
        "/Cf3a8T1iqEqNKGg+HwEUcNW0Wlj07tSOQ7/zEqUzNXunh3Mdj3j0niu6VqIqo32" + \
        "uNrgB/Sys/ULAwK99pN38MAiQV8UGQSzftEdrJyJ/HlFWiTISdqR3njzM9BwfPGe" + \
        "7OuHZnRsukPSOt1FGj5L6WOSvzd4RnYSZZLWU+PcOiZvcJ6NwF/BWKxve6x+lmGO" + \
        "VqYt83sYAtRymWjbpvZ3YZEn3j0b+olZ/QBT0NOXLT5QBNiDLFbq04mmqPpH9Sgh" + \
        "se7xr/LnCI2RgGurSwLkAgNiq8+13+y659DJQ9xMbCvlYVFpy10Yd8yIpHodxAUz" + \
        "twIDAQAB" + \
        "\n-----END PUBLIC KEY-----"

    alipay = AliPay(
        appid="2021000147696674",  # APPID(上线之后需要改成，真实应用的appid)
        app_notify_url=None,  # 应用回调地址[支付成功以后,支付宝返回结果到哪一个地址下面]
        app_private_key_string=app_private_key_string,  # 自己生成的私钥
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认 False
        verbose=False,  # 输出调试数据
        config=AliPayConfig(timeout=120)  # 可选，请求超时时间
    )
    return alipay

# 后端回调地址
pay_notify_url="http://8.137.105.108:377/alipay/result"
# 前端回调地址
pay_return_url="http://8.137.105.108:777/payresult"