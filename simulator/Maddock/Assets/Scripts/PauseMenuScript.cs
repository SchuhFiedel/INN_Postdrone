using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PauseMenuScript : MonoBehaviour
{
    // Start is called before the first frame update

    public GameObject pausePanel;
    public static bool isPaused;

    private void Start()
    {
        isPaused = false;
    }

    

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            
         //   Debug.Log(isPaused);

            if (!isPaused)
            {
                Pause();
            }
            /*else
            {
                Resume();
            }*/
        }
    }

    public void Resume()
    {
        pausePanel.SetActive(false);
        Time.timeScale = 1;
        //lookscript.enabled = true;
        isPaused = false;
       // Debug.Log("Resume");
    }

    public void Pause()
    {
        pausePanel.SetActive(true);
        Time.timeScale = 0;
        //lookscript.enabled = false;
        isPaused = true;
       // Debug.Log("Pause");
    }

    public void CloseApplication()
    {
      //  Debug.Log("Quit");
        Application.Quit();
    }

}
