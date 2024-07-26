# satellite-register.sh, satellite-register.py

## 目的

satellite-register.sh と satellite-register.py は、RHEL サーバ (クライアントホスト)を Red Hat Satellite サーバに登録するためのシェルまたは Python スクリプトです。
従来の katello-consumer-ca-latest.noarch.rpm を http://satellite.example.com/pub/ からダウンロードしてインストールし、subscription-manager register コマンドで登録する方法が非推奨 (deprecated) となっておりますので、それに代わる方法として、現在もサポートされている方法を組み合わせて簡単に実行することを目的としたスクリプトとなります。

## 制限・制約

satellite-register.sh は、Satellite API を使って登録用コマンドラインを生成します。登録用コマンドラインは API 呼び出しの結果 JSON 形式で返されますが、本シェルスクリプトは簡易な実装で、JSON データを正確に解釈して必要なコマンドライン文字列を取り出しているわけではありませんので、API から返される JSON の文字列パターンが現在想定している形式から変化した場合に、正しい動作をしなくなる可能性があります。
JSON データを正しく解釈して実行するためには、Python 等の軽量言語で JSON データを読み込んで必要な属性に与えられた値だけを抽出するコードを実装する必要があります。

satellite-register.py は、最小構成でインストールした RHEL 8/9 上の /usr/libexec/platform-python で動作を確認済みで、API から返される JSON データを解釈して登録用コマンドを取り出し、実行していますので、satellite-register.sh よりは安全と考えられます。

ただし、本スクリプトはサンプル実装として提供されており、一切の保証はありません。また、製品に含まれる提供物の一部ではありませんので、当然ながら弊社の製品サポート対象外です。よって、サポートケースによる製品サポート窓口への本スクリプトに関するお問い合わせはご遠慮ください。Red Hat コンサルティングへお問い合わせいただく場合は、有効な有償サービス契約が必要で、ご契約時間から稼動時間を消費する前提での有償サービスとしての対応となり、それ以外のサポート・ご支援の提供はありません。

## 前提条件

* 登録する Satellite サーバ側で、ホスト登録用ユーザが登録されていること
* ホスト登録用ユーザ作成時に、"Register hosts" ロールだけを割り当てていること
* Satellite にはクライアントホストが使用するサブスクリプションと紐づいたアクティベーションキーが作成されていること
* クライアントホストから Satellite へ、http/https で接続可能であること
* クライアントホストに bash、curl、sed の各標準 Linux コマンドがインストール済みであること

## 使用法

1. satellite-register.sh および satellite-register.py を編集して、`#### MINIMUM CONFIGURATION PARAMETERS` の下の変数4つを、それぞれお使いの Satellite サーバの FQDN (または IP アドレス)、ホスト登録用ユーザ名、同パスワード、アクティベーションキー名に変更してください。

```
#### MINIMUM CONFIGURATION PARAMETERS
# REPLACE THESE VALUES WITH YOUR SATELLITE SERVER'S BEFORE DISTRIBUTING
sat_hostname='satellite.fqdn'
sat_username='username'
sat_password='password'
sat_activation_key='activation-key'
```

注: sat_hostname に FQDN ではなく IP アドレスを指定すると、登録用コマンド実行途中でエラーが発生し、異常終了しますが、ホスト登録自体はできているはずなので、ホスト登録が確認できればエラーそのものは無視していただいて構いません。

2. 必要がある場合は、`#### Configurable Registration Parameters (Optional)` 以降の変数4つを編集してください。Satellite を単なる yum リポジトリとして利用するだけの場合は、以下のデフォルト値から変更する必要はありません。

```
#### Configurable Registration Parameters (Optional)
# insecure: true if Satellite server uses Self-Signed Certificate, False if not
insecure='true'
# insights: true if you want host to register to Red Hat Insights at registration time
insights='false'
# remote_exec: true if you plan to run commands on host from Satellite (requires ssh port open on host)
remote_exec='false'
# remote_exec_pull: true if you plan to run commands on host from Satellite in pull mode (does not require ssh port open on host; host subscribes to MQTT broker to receive remote execution job notifications)
remote_exec_pull='false'
```

※ satellite-register.py の場合は、変数に設定すべき値は True または False と、引用符は不要で先頭を大文字としてください。

3. 編集したファイル satellite-register.sh と satellite-register.py を、Satellite サーバの /var/www/html/pub にコピーしてください。ファイルのパーミッションは全ユーザへの読み出し許可が必要ですので、適宜 `chmod` コマンドで変更してください。

4. ホストを登録する際には、登録しようとしているホスト上で、以下のコマンドを root 権限で実行してください。

RHEL 7 ホストの場合:
```
curl -o satellite-register.sh http://satellite.fqdn/pub/satellite-register.sh
bash ./satellite-register.sh
```

RHEL 8/9 ホストの場合:
```
curl -o satellite-register.py http://satellite.fqdn/pub/satellite-register.py
/usr/libexec/platform-python ./satellite-register.py
```
