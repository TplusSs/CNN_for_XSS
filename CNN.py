import time
import numpy as np
from sklearn.metrics import precision_score,recall_score
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense,InputLayer,Dropout,LSTM,Conv1D,Flatten,GlobalAveragePooling1D,MaxPool1D
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from Preprocessing_data import build_dataset
from utils import init_session
init_session()
batch_size=128
epochs_num=1
process_datas_dir="file\\process_datas.pickle"
log_dir="log\\Conv.log"
model_dir="file\\Conv_model"
def train(train_generator,train_size,input_num,dims_num):
    print("Start Train Job! ")
    start=time.time()
    inputs=InputLayer(input_shape=(input_num,dims_num),batch_size=batch_size)
    layer1=Conv1D(64,3,activation="relu")
    layer2=Conv1D(64,3,activation="relu")
    layer3=Conv1D(128,3,activation="relu")
    layer4=Conv1D(128,3,activation="relu")
    layer5=Dense(128,activation="relu")
    output=Dense(2,activation="softmax",name="Output")
    optimizer=Adam()
    model=Sequential()
    model.add(inputs)
    model.add(layer1)
    model.add(layer2)
    model.add(MaxPool1D(pool_size=2))
    model.add(Dropout(0.5))
    model.add(layer3)
    model.add(layer4)
    model.add(MaxPool1D(pool_size=2))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(layer5)
    model.add(Dropout(0.5))
    model.add(output)
    call=TensorBoard(log_dir=log_dir,write_grads=True, write_graph=True, write_images=True)
    model.compile(optimizer,loss="categorical_crossentropy",metrics=["accuracy"])
    #model.fit_generator(train_generator,steps_per_epoch=train_size//batch_size,epochs=epochs_num,callbacks=[call])
    model.fit_generator(train_generator, steps_per_epoch=3, epochs=366, callbacks=[call])
    model.save(model_dir)
    end=time.time()
    print("Over train job in %f s"%(end-start))
    
def test(model_dir,test_generator,test_size,input_num,dims_num,batch_size):
    model=load_model(model_dir)
    labels_pre=[]
    labels_true=[]
    batch_num=test_size//batch_size+1
    steps=0
    for batch,labels in test_generator:
        if len(labels)==batch_size:
            labels_pre.extend(model.predict_on_batch(batch))
        else:
            batch=np.concatenate((batch,np.zeros((batch_size-len(labels),input_num,dims_num))))
            labels_pre.extend(model.predict_on_batch(batch)[0:len(labels)])
        labels_true.extend(labels)
        steps+=1
        print("%d/%d batch"%(steps,batch_num))
    labels_pre=np.array(labels_pre).round()
    def to_y(labels):
        y=[]
        for i in range(len(labels)):
            if labels[i][0]==1:
                y.append(0)
            else:
                y.append(1)
        return y
    y_true=to_y(labels_true)
    y_pre=to_y(labels_pre)
    precision=precision_score(y_true,y_pre)
    recall=recall_score(y_true,y_pre)
    print("Precision score is :",precision)
    print("Recall score is :",recall)
    
if __name__=="__main__":
    train_generator, test_generator, train_size, test_size, input_num, dims_num=build_dataset(batch_size)
    train(train_generator,train_size,input_num,dims_num)
    test(model_dir,test_generator,test_size,input_num,dims_num,batch_size)
