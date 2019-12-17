# CNN_for_XSS

说明：

本项目通过神经网络算法来检测web攻击。
由于Web攻击种类众多，本文主要选择OWASP TOP 10中的跨站脚本攻击（XSS）作为主要检测对象进行研究。
使用Word2Vec建立词向量模型，并使用TSNE算法进行降维，分别使用卷积神经网络、时间循环神经网络、多层神经网络三种算法检测入侵行为。

环境

tensorflow 1.13.1
tensorboard 1.13.1
keras 2.1.0
        
运行
	
word2vec_ginsim.py训练嵌入式词向量
processing.py预处理数据，生成训练数据和测试数据。
CNN.py使用卷积神经网络训练模型，在测试集上测试准确率和召回率。

