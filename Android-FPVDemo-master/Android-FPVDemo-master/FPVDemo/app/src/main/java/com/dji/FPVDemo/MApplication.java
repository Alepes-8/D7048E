package com.dji.FPVDemo;

import android.app.Application;
import android.content.Context;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.secneo.sdk.Helper;

public class MApplication extends Application {

    private FPVDemoApplication fpvDemoApplication;
    @Override
    protected void attachBaseContext(Context paramContext) {
        super.attachBaseContext(paramContext);
        Helper.install(MApplication.this);
        if (fpvDemoApplication == null) {
            fpvDemoApplication = new FPVDemoApplication();
            fpvDemoApplication.setContext(this);
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        if(!Python.isStarted()){
            Python.start(new AndroidPlatform(this));
        }
        fpvDemoApplication.onCreate();
    }
}
