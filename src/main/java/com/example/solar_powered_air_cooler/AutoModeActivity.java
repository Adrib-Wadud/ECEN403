package com.example.solar_powered_air_cooler;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class AutoModeActivity extends AppCompatActivity {
    public BluetoothSocket btSocket = MainActivity.btSocket;
    public String chargeLevel = "0";
    public Boolean autoModeActivated = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_auto_mode);
        chargeLevel = getIntent().getExtras().getString("Charge");
        TextView charge = (TextView)findViewById(R.id.charge_level_auto);
        charge.setText(chargeLevel);
    }

    public void activateAutoMode(View v){

        if(btSocket!=null) {

                MainActivity.sendMessageToServer("Activate Auto Mode!");
                String message = MainActivity.recvdMessageFromServer();
                TextView mode_activated = (TextView)findViewById(R.id.textView22);
                mode_activated.setText("Auto mode activated");
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();
                autoModeActivated = true;
                MainActivity.sendMessageToServer("Get set temperature!");
                String set_temperature = MainActivity.recvdMessageFromServer();
                TextView temperature = (TextView)findViewById(R.id.set_temp);
                temperature.setText(set_temperature);

                MainActivity.sendMessageToServer("Get set humidity!");
                String set_humidity = MainActivity.recvdMessageFromServer();
                TextView humidity = (TextView)findViewById(R.id.set_humidity);
                humidity.setText(set_humidity);
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }

    public void deactivateAutoMode(View v){
        if(btSocket!=null) {
            MainActivity.sendMessageToServer("Deactivate Auto Mode!");
            TextView mode_activated = (TextView)findViewById(R.id.textView22);
            mode_activated.setText("Auto mode not activated");
            String message = MainActivity.recvdMessageFromServer();
            Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
            toast.show();
            autoModeActivated = false;
        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }

    }


    public void temperatureUp(View v){

        if(btSocket!=null) {
            if(autoModeActivated){
                MainActivity.sendMessageToServer("Temperature Up!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get set temperature!");
                String updated_temp = MainActivity.recvdMessageFromServer();
                TextView temperature = (TextView)findViewById(R.id.set_temp);
                temperature.setText(updated_temp);

            }
            else{
                Toast toast = Toast.makeText(this, "Auto mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }



        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void temperatureDown(View v){

        if(btSocket!=null) {
            if(autoModeActivated){
                MainActivity.sendMessageToServer("Temperature Down!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get set temperature!");
                String updated_temp = MainActivity.recvdMessageFromServer();
                TextView temperature = (TextView)findViewById(R.id.set_temp);
                temperature.setText(updated_temp);

            }
            else{
                Toast toast = Toast.makeText(this, "Auto mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void humidityUp(View v){

        if(btSocket!=null) {
            if(autoModeActivated){
                MainActivity.sendMessageToServer("Humidity Up!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get set humidity!");
                String updated_humid = MainActivity.recvdMessageFromServer();
                TextView temperature = (TextView)findViewById(R.id.set_humidity);
                temperature.setText(updated_humid);

            }
            else{
                Toast toast = Toast.makeText(this, "Auto mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }


        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    public void humidityDown(View v){

        if(btSocket!=null) {
            if(autoModeActivated){
                MainActivity.sendMessageToServer("Humidity Down!");
                String message = MainActivity.recvdMessageFromServer();
                Toast toast = Toast.makeText(this, message, Toast.LENGTH_SHORT);
                toast.show();

                MainActivity.sendMessageToServer("Get set humidity!");
                String updated_humid = MainActivity.recvdMessageFromServer();
                TextView temperature = (TextView)findViewById(R.id.set_humidity);
                temperature.setText(updated_humid);

            }
            else{
                Toast toast = Toast.makeText(this, "Auto mode not activated", Toast.LENGTH_SHORT);
                toast.show();
            }

        }
        else{
            Toast toast = Toast.makeText(this, "Blueotooth connection not established", Toast.LENGTH_SHORT);
            toast.show();
        }
    }
}
